from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect ComfyUI workflow nodes and patchable inputs.")
    parser.add_argument("workflow", type=Path)
    args = parser.parse_args()

    data = json.loads(args.workflow.read_text(encoding="utf-8"))

    if _is_api_workflow(data):
        _print_api_workflow(data)
        return

    if isinstance(data, dict) and isinstance(data.get("nodes"), list):
        _print_ui_workflow(data)
        return

    raise SystemExit("Unsupported workflow format. Expected ComfyUI API prompt JSON or UI workflow JSON.")


def _is_api_workflow(data: Any) -> bool:
    return isinstance(data, dict) and all(
        isinstance(node, dict) and "class_type" in node and "inputs" in node
        for node in data.values()
    )


def _print_api_workflow(data: dict[str, Any]) -> None:
    print("Detected ComfyUI API prompt format.")
    for node_id, node in data.items():
        class_type = node.get("class_type", "")
        print(f"\n[{node_id}] {class_type}")
        inputs = node.get("inputs") or {}
        for key, value in inputs.items():
            if _is_link(value):
                continue
            print(f"  {node_id}.inputs.{key} = {_safe_repr(value)}")


def _print_ui_workflow(data: dict[str, Any]) -> None:
    print("Detected ComfyUI UI workflow format.")
    print("Use this in the ComfyUI editor, then export Save (API Format) for backend use.")
    for node in data["nodes"]:
        node_id = node.get("id")
        node_type = node.get("type")
        title = node.get("title")
        print(f"\n[{node_id}] {node_type}" + (f" - {title}" if title else ""))
        for index, value in enumerate(node.get("widgets_values") or []):
            print(f"  widgets_values[{index}] = {_safe_repr(value)}")


def _is_link(value: Any) -> bool:
    return (
        isinstance(value, list)
        and len(value) == 2
        and isinstance(value[0], str)
        and isinstance(value[1], int)
    )


def _safe_repr(value: Any) -> str:
    return repr(value).encode("ascii", "backslashreplace").decode("ascii")


if __name__ == "__main__":
    main()
