from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_workflow(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}

    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Workflow file must contain a JSON object: {path}")

    return data
