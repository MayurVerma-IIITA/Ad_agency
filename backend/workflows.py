from __future__ import annotations

import json
import copy
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


def apply_workflow_patches(workflow: dict[str, Any], patches: dict[str, Any]) -> dict[str, Any]:
    patched = copy.deepcopy(workflow)
    for path, value in patches.items():
        _set_dotted_path(patched, path, value)
    return patched


def request_workflow_values(request: Any) -> dict[str, Any]:
    return {
        "prompt": request.prompt,
        "negative_prompt": request.negative_prompt,
        "duration": request.duration,
        "width": request.width,
        "height": request.height,
        "fps": request.fps,
        "mode": request.mode.value,
        "image_asset_id": request.image_asset_id,
    }


def resolve_workflow_patch_values(patches: dict[str, str], request: Any) -> dict[str, Any]:
    values = request_workflow_values(request)
    resolved: dict[str, Any] = {}
    for workflow_path, request_key in patches.items():
        if request_key not in values:
            raise ValueError(f"Unsupported workflow patch request key: {request_key}")
        resolved[workflow_path] = values[request_key]
    return resolved


def _set_dotted_path(target: dict[str, Any], path: str, value: Any) -> None:
    if not path:
        raise ValueError("Workflow patch path cannot be empty")

    parts = path.split(".")
    current: Any = target
    for part in parts[:-1]:
        if isinstance(current, list):
            current = _list_item(current, part, path)
            continue

        if not isinstance(current, dict):
            raise ValueError(f"Cannot traverse non-object while applying workflow patch: {path}")
        if part not in current:
            raise ValueError(f"Workflow patch path not found: {path}")
        current = current[part]

    last = parts[-1]
    if isinstance(current, list):
        index = _list_index(last, path)
        current[index] = value
        return

    if not isinstance(current, dict):
        raise ValueError(f"Cannot set value on non-object while applying workflow patch: {path}")
    if last not in current:
        raise ValueError(f"Workflow patch path not found: {path}")
    current[last] = value


def _list_item(items: list[Any], part: str, path: str) -> Any:
    return items[_list_index(part, path)]


def _list_index(part: str, path: str) -> int:
    try:
        index = int(part)
    except ValueError as exc:
        raise ValueError(f"Workflow patch list path segment must be an integer: {path}") from exc
    return index
