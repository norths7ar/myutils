import json
from collections.abc import Iterable
from pathlib import Path
from typing import Generator


def load_json(path: Path):
    """Load data from a JSON file."""
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def save_json(some_item, path: Path):
    """Save data to a JSON file."""
    with path.open('w', encoding='utf-8') as f:
        json.dump(some_item, f, ensure_ascii=False, indent=2)


def load_jsonl(file_path: Path) -> list:
    """Load data from a JSON line (JSONL) file."""
    with file_path.open('r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def iter_jsonl(file_path: Path) -> Generator:
    """Yield a generator of jsonl file."""
    with file_path.open('r', encoding='utf-8') as f:
        for line in f:
            yield json.loads(line)


def add_to_jsonl(items: Iterable, path: Path):
    """Append items to a jsonl file."""
    with path.open("a", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def save_jsonl(items: Iterable, path: Path):
    """Save items to a jsonl file."""
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def load_md(file_path: Path) -> str:
    """Load data from a Markdown (MD) file."""
    with file_path.open('r', encoding='utf-8') as f:
        return f.read()


def set_output_dir(path: Path):
    """Set the output directory for the current step."""
    path.mkdir(parents=True, exist_ok=True)
    return path
