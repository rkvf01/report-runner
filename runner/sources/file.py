import json
from pathlib import Path


def fetch_file_source(source_config: dict) -> dict:
    path = source_config.get("path")

    if not path:
        raise ValueError("File source is missing required field: path")

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File source not found: {path}")

    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)