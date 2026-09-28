from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from backend.comfy.client import ComfyUIClient
from backend.model_registry import ModelRegistry
from backend.models import CommercialStatus, ModelRegistryEntry, VideoGenerationRequest
from backend.providers.wan import WanProvider


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
