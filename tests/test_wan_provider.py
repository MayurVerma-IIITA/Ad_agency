from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest

from backend.comfy.client import ComfyUIClient
from backend.model_registry import ModelRegistry
from backend.models import CommercialStatus, ModelRegistryEntry, VideoGenerationRequest
from backend.providers.wan import WanProvider
from backend.storage import LocalAssetStore


@pytest.mark.asyncio
async def test_get_result_maps_comfyui_mp4_to_video_asset() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/history/prompt_123"
        return httpx.Response(
            200,
            json={
                "prompt_123": {
                    "outputs": {
                        "9": {
                            "gifs": [
                                {
                                    "filename": "ad.mp4",
                                    "subfolder": "campaign-a",
                                    "type": "output",
                                }
                            ]
                        }
                    }
                }
            },
        )

    provider = WanProvider(
        ComfyUIClient("http://testserver", transport=httpx.MockTransport(handler)),
        workflow_template={"1": {"class_type": "Mock"}},
        model_registry=ModelRegistry(
            [
                ModelRegistryEntry(
                    model_id="wan_test",
                    name="Wan Test",
                    provider="wan",
                    type="video",
                    capabilities=["text_to_video"],
                    license="Apache-2.0",
                    commercial_status=CommercialStatus.APPROVED,
                )
            ]
        ),
    )

    request = VideoGenerationRequest(
        prompt="cinematic perfume advertisement",
        negative_prompt="low quality",
        duration=7,
        width=720,
        height=1280,
        fps=24,
    )

    asset = await provider.get_result("prompt_123", request)

    assert asset.type == "video"
    assert asset.file_path == Path("comfyui/output/campaign-a/ad.mp4")
    assert asset.provider == "wan"
    assert asset.model == "wan_test"
    assert asset.license == "Apache-2.0"
    assert asset.prompt == "cinematic perfume advertisement"
    assert asset.parameters["provider_job_id"] == "prompt_123"
    assert asset.parameters["node_id"] == "9"
    assert asset.parameters["output_kind"] == "gifs"
    assert asset.parameters["request"]["negative_prompt"] == "low quality"
    assert asset.parameters["request"]["duration"] == 7
    assert asset.parameters["model"]["commercial_status"] == "approved"


@pytest.mark.asyncio
async def test_get_result_downloads_output_into_asset_store(tmp_path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/history/prompt_123":
            return httpx.Response(
                200,
                json={
                    "prompt_123": {
                        "outputs": {
                            "9": {
                                "gifs": [
                                    {
                                        "filename": "ad.mp4",
                                        "subfolder": "",
                                        "type": "output",
                                    }
                                ]
                            }
                        }
                    }
                },
            )
        if request.url.path == "/view":
            assert request.url.params["filename"] == "ad.mp4"
            return httpx.Response(200, content=b"video bytes")
        return httpx.Response(404)

    provider = WanProvider(
        ComfyUIClient("http://testserver", transport=httpx.MockTransport(handler)),
        workflow_template={"1": {"class_type": "Mock"}},
        model_registry=ModelRegistry(
            [
                ModelRegistryEntry(
                    model_id="wan_test",
                    name="Wan Test",
                    provider="wan",
                    type="video",
                    capabilities=["text_to_video"],
                    license="Apache-2.0",
                    commercial_status=CommercialStatus.APPROVED,
                )
            ]
        ),
        asset_store=LocalAssetStore(tmp_path),
    )

    asset = await provider.get_result("prompt_123", VideoGenerationRequest(prompt="ad"))

    assert asset.file_path.parent == tmp_path / asset.asset_id
    assert asset.file_path.name == "ad.mp4"
    assert asset.file_path.read_bytes() == b"video bytes"


@pytest.mark.asyncio
async def test_generate_text_to_video_applies_metadata_workflow_patches() -> None:
    captured_workflow = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_workflow
        assert request.url.path == "/prompt"
        captured_workflow = json.loads(request.content)["prompt"]
        return httpx.Response(200, json={"prompt_id": "prompt_123"})

    provider = WanProvider(
        ComfyUIClient("http://testserver", transport=httpx.MockTransport(handler)),
        workflow_template={
            "6": {"inputs": {"text": "old prompt"}},
            "7": {"inputs": {"width": 512, "height": 512, "fps": 12}},
        },
        model_registry=ModelRegistry(
            [
                ModelRegistryEntry(
                    model_id="wan_test",
                    name="Wan Test",
                    provider="wan",
                    type="video",
                    capabilities=["text_to_video"],
                    license="Apache-2.0",
                    commercial_status=CommercialStatus.APPROVED,
                )
            ]
        ),
    )

    await provider.generate_text_to_video(
        VideoGenerationRequest(
            prompt="cinematic perfume advertisement",
            width=720,
            height=1280,
            fps=24,
            metadata={
                "workflow_patches": {
                    "6.inputs.text": "prompt",
                    "7.inputs.width": "width",
                    "7.inputs.height": "height",
                    "7.inputs.fps": "fps",
                }
            },
        )
    )

    assert captured_workflow["6"]["inputs"]["text"] == "cinematic perfume advertisement"
    assert captured_workflow["7"]["inputs"]["width"] == 720
    assert captured_workflow["7"]["inputs"]["height"] == 1280
    assert captured_workflow["7"]["inputs"]["fps"] == 24
