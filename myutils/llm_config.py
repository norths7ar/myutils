import logging
import re
import time
from dataclasses import dataclass, field
from typing import Any
from iEnigma import UnifiedLLM # iEnigma is an internal library for LLM queries.

DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODEL = "claude-sonnet-4-20250514"


def clean_json_identifier(response: str) -> str:
    """
    Clean the JSON response from GPT to extract valid JSON content.
    This function handles cases where GPT outputs ```json ... ``` blocks.
    """
    match = re.search(r"```json\s*(.*?)\s*```", response, re.DOTALL)
    if match:
        return match.group(1).strip()

    # If there's an opening ```json but no closing ```
    json_start = response.find("```json")
    if json_start != -1:
        return response[json_start+7:].strip()

    return response  # If no special formatting, return as is


@dataclass
class LLMConfig:
    """Data class for storing configuration parameters for the language model."""
    provider: str = DEFAULT_PROVIDER
    model_name: str = DEFAULT_MODEL
    max_retries: int = 5
    extra_params: dict[str, Any] = field(default_factory=lambda: {
        "max_tokens": 8192,
        "temperature": 1
    })
    @property
    def model(self):
        """Generate model name for function calling"""
        return f"{self.provider}::{self.model_name}"

    def get_api_params(self):
        """Return API parameters, ensuring no None values."""
        return {k: v for k, v in self.extra_params.items() if v is not None}

    def update(self, **kwargs):
        """Dynamically update configuration parameters."""
        self.extra_params.update(kwargs)


def create_llm_config(
        provider: str = DEFAULT_PROVIDER,
        model_name: str = DEFAULT_MODEL,
        **kwargs
) -> LLMConfig:
    """
    Create an LLMConfig object with the specified parameters.
    Args:
        provider (str): The provider of the language model.
        model_name (str): The name of the language model.
        **kwargs: Additional keyword arguments for the LLMConfig object.
    Returns:
        LLMConfig: The LLMConfig object with the specified parameters.
    """
    config = LLMConfig(provider=provider, model_name=model_name)
    config.update(**kwargs)
    return config


def get_llm_response(user_prompt: str,
                     *, # Enforce keyword arguments for the remaining parameters
                     api_key: str,
                     config: LLMConfig,
                     system_prompt: str = "",
                     logger: logging.Logger) -> str:
    """
    Generates a response from a language model based on the provided user prompt.
    Args:
        user_prompt (str): The user prompt to generate a response for.
        system_prompt (str): The system prompt to provide context for the response.
        config (LLMConfig or dict): The configuration parameters for the language model.
    Returns:
        str: The generated response from the language model.
    Raises:
        Exception: If the response generation fails after the maximum number of retries.
    """
    params = {
        "messages": []
    }

    if system_prompt:
        params["messages"].append({"role": "developer", "content": system_prompt})
    params["messages"].append({"role": "user", "content": user_prompt})
    params.update(config.get_api_params())

    llm = UnifiedLLM(api_key=api_key)
    last_error = None

    for attempt in range(config.max_retries):
        try:
            response = llm.unified_completion(config.model, **params)
            return response['result']['content']['content']
        except Exception as e:
            last_error = e

            if logger:
                logger.warning("Attempt %d failed with error %s.", attempt + 1, e)
            else:
                print(f"Attempt {attempt + 1} failed with error {e}.")

            if attempt < config.max_retries - 1:
                wait_time = 5 * (2 ** attempt)
                if logger:
                    logger.info("Retrying after %d seconds...", wait_time)
                else:
                    print(f"Retrying after {wait_time} seconds...")
                time.sleep(wait_time)

    assert last_error is not None # Protection line to avoid PyLance type checking
    raise last_error
