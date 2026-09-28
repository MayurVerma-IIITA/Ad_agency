from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from backend.comfy.client import ComfyUIClient
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
    )

    asset = await provider.get_result("prompt_123")

    assert asset.type == "video"
    assert asset.file_path == Path("comfyui/output/campaign-a/ad.mp4")
    assert asset.provider == "wan"
    assert asset.model == "wan"
    assert asset.parameters["provider_job_id"] == "prompt_123"
    assert asset.parameters["node_id"] == "9"
    assert asset.parameters["output_kind"] == "gifs"
