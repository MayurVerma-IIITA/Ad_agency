from __future__ import annotations

import pytest

from backend.model_registry import ModelRegistry
from backend.models import CommercialStatus, ModelRegistryEntry, VideoGenerationRequest


def test_select_auto_model_for_development_use() -> None:
    registry = ModelRegistry(
        [
            ModelRegistryEntry(
                model_id="wan_dev",
                name="Wan Dev",
                provider="wan",
                type="video",
                capabilities=["text_to_video"],
                license="unknown",
                commercial_status=CommercialStatus.UNKNOWN,
            )
        ]
    )

    selected = registry.select_video_model(VideoGenerationRequest(prompt="ad"), provider="wan")

    assert selected.model_id == "wan_dev"


def test_commercial_request_rejects_unknown_model() -> None:
    registry = ModelRegistry(
        [
            ModelRegistryEntry(
                model_id="wan_dev",
                name="Wan Dev",
                provider="wan",
                type="video",
                capabilities=["text_to_video"],
                license="unknown",
                commercial_status=CommercialStatus.UNKNOWN,
            )
        ]
    )

    request = VideoGenerationRequest(prompt="client ad", commercial_use=True)

    with pytest.raises(ValueError, match="commercial use"):
        registry.select_video_model(request, provider="wan")


def test_explicit_model_must_support_requested_mode() -> None:
    registry = ModelRegistry(
        [
            ModelRegistryEntry(
                model_id="wan_t2v",
                name="Wan Text",
                provider="wan",
                type="video",
                capabilities=["text_to_video"],
                license="unknown",
                commercial_status=CommercialStatus.UNKNOWN,
            )
        ]
    )

    request = VideoGenerationRequest(prompt="client ad", model="wan_t2v", mode="image_to_video", image_asset_id="asset_1")

    with pytest.raises(ValueError, match="does not support"):
        registry.select_video_model(request, provider="wan")
