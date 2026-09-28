from __future__ import annotations

import json

import pytest

from backend.workflows import load_workflow


def test_load_workflow_returns_empty_dict_without_path() -> None:
    assert load_workflow(None) == {}


def test_load_workflow_reads_json_object(tmp_path) -> None:
    workflow_path = tmp_path / "workflow.json"
    workflow_path.write_text(json.dumps({"1": {"class_type": "CheckpointLoaderSimple"}}), encoding="utf-8")

    workflow = load_workflow(workflow_path)

    assert workflow["1"]["class_type"] == "CheckpointLoaderSimple"


def test_load_workflow_rejects_non_object_json(tmp_path) -> None:
    workflow_path = tmp_path / "workflow.json"
    workflow_path.write_text("[]", encoding="utf-8")

    with pytest.raises(ValueError):
        load_workflow(workflow_path)
