import re

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
