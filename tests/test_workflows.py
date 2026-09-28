from __future__ import annotations

import json

import pytest

from backend.models import VideoGenerationRequest
from backend.workflows import apply_workflow_patches, load_workflow, resolve_workflow_patch_values


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


def test_apply_workflow_patches_updates_nested_values_without_mutating_original() -> None:
    workflow = {
        "6": {"inputs": {"text": "old prompt", "size": [512, 512]}},
        "7": {"inputs": {"fps": 12}},
    }

    patched = apply_workflow_patches(
        workflow,
        {
            "6.inputs.text": "new prompt",
            "6.inputs.size.0": 720,
            "6.inputs.size.1": 1280,
            "7.inputs.fps": 24,
        },
    )

    assert patched["6"]["inputs"]["text"] == "new prompt"
    assert patched["6"]["inputs"]["size"] == [720, 1280]
    assert patched["7"]["inputs"]["fps"] == 24
    assert workflow["6"]["inputs"]["text"] == "old prompt"


def test_apply_workflow_patches_rejects_missing_path() -> None:
    with pytest.raises(ValueError, match="not found"):
        apply_workflow_patches({"6": {"inputs": {}}}, {"6.inputs.text": "prompt"})


def test_resolve_workflow_patch_values_from_request() -> None:
    request = VideoGenerationRequest(prompt="ad", width=720, height=1280, fps=24)

    resolved = resolve_workflow_patch_values(
        {
            "6.inputs.text": "prompt",
            "7.inputs.width": "width",
            "7.inputs.height": "height",
            "8.inputs.fps": "fps",
        },
        request,
    )

    assert resolved == {
        "6.inputs.text": "ad",
        "7.inputs.width": 720,
        "7.inputs.height": 1280,
        "8.inputs.fps": 24,
    }
