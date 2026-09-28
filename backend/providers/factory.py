from __future__ import annotations

from backend.comfy.client import ComfyUIClient
from backend.config import Settings
from backend.model_registry import ModelRegistry
from backend.providers.base import VideoProvider
from backend.providers.wan import WanProvider
from backend.storage import LocalAssetStore
from backend.workflows import load_workflow


def build_video_provider(settings: Settings) -> VideoProvider:
    provider_name = settings.video_provider.lower()

    if provider_name == "wan":
        return WanProvider(
            comfyui=ComfyUIClient(settings.comfyui_base_url),
            workflow_template=load_workflow(settings.wan_workflow_path),
            model_registry=ModelRegistry.from_file(settings.model_registry_path),
            asset_store=LocalAssetStore(settings.asset_root),
        )

    raise ValueError(f"Unsupported VIDEO_PROVIDER: {settings.video_provider}")
