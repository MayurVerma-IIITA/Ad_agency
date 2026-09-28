from __future__ import annotations

import copy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.comfy.client import ComfyUIClient
from backend.model_registry import ModelRegistry
from backend.models import ModelRegistryEntry
from backend.models import AssetRecord, JobRecord, JobStatus, VideoGenerationRequest
from backend.providers.base import VideoProvider


class WanProvider(VideoProvider):
    """Wan video provider backed by ComfyUI workflows.

    The workflow translation is deliberately isolated here so the API, MCP
    tools, and job manager do not become Wan-specific.
    """

    name = "wan"

    def __init__(
        self,
        comfyui: ComfyUIClient,
        workflow_template: dict[str, Any] | None = None,
        model_registry: ModelRegistry | None = None,
    ) -> None:
        self.comfyui = comfyui
        self.workflow_template = workflow_template or {}
        self.model_registry = model_registry

    async def generate_text_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        model = self._select_model(request)
        workflow = self._build_workflow(request, model)
        provider_job_id = await self.comfyui.submit_prompt(workflow)
        return JobRecord(
            status=JobStatus.RUNNING,
            request=request,
            provider_job_id=provider_job_id,
        )

    async def generate_image_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        if not request.image_asset_id:
            raise ValueError("image_asset_id is required for image-to-video generation")
        model = self._select_model(request)
        workflow = self._build_workflow(request, model)
        provider_job_id = await self.comfyui.submit_prompt(workflow)
        return JobRecord(
            status=JobStatus.RUNNING,
            request=request,
            provider_job_id=provider_job_id,
        )

    async def get_status(self, provider_job_id: str) -> JobRecord:
        history = await self.comfyui.get_history(provider_job_id)
        completed = bool(history.get(provider_job_id, {}).get("outputs"))
        placeholder_request = VideoGenerationRequest(prompt="provider status lookup")
        return JobRecord(
            status=JobStatus.COMPLETED if completed else JobStatus.RUNNING,
            request=placeholder_request,
            provider_job_id=provider_job_id,
            updated_at=datetime.now(timezone.utc),
        )

    async def get_result(self, provider_job_id: str, request: VideoGenerationRequest) -> AssetRecord:
        model = self._select_model(request)
        history = await self.comfyui.get_history(provider_job_id)
        output = _first_output_file(history, provider_job_id)
        filename = output["filename"]
        subfolder = output.get("subfolder") or ""
        file_type = _asset_type_from_filename(filename)

        return AssetRecord(
            type=file_type,
            file_path=Path("comfyui") / str(output.get("type", "output")) / subfolder / filename,
            provider=self.name,
            model=model.model_id,
            prompt=request.prompt,
            parameters={
                "provider_job_id": provider_job_id,
                "node_id": output.get("node_id"),
                "output_kind": output.get("output_kind"),
                "comfyui_type": output.get("type"),
                "request": request.model_dump(mode="json"),
                "model": model.model_dump(mode="json"),
            },
            license=model.license,
        )

    def _build_workflow(self, request: VideoGenerationRequest, model: ModelRegistryEntry) -> dict[str, Any]:
        if not self.workflow_template:
            raise ValueError("Wan workflow template is not configured")

        workflow = copy.deepcopy(self.workflow_template)
        workflow["_agency_request"] = request.model_dump(mode="json")
        workflow["_agency_model"] = model.model_dump(mode="json")
        return workflow

    def _select_model(self, request: VideoGenerationRequest) -> ModelRegistryEntry:
        if self.model_registry:
            return self.model_registry.select_video_model(request, provider=self.name)

        return ModelRegistryEntry(
            model_id="wan",
            name="Wan",
            provider=self.name,
            type="video",
            capabilities=[request.mode.value],
            license="unknown",
            commercial_status="unknown",
        )


def _first_output_file(history: dict[str, Any], provider_job_id: str) -> dict[str, Any]:
    job = history.get(provider_job_id)
    if not job:
        raise ValueError(f"ComfyUI history did not include prompt id: {provider_job_id}")

    outputs = job.get("outputs") or {}
    for node_id, node_outputs in outputs.items():
        for output_kind in ("gifs", "videos", "images", "audio"):
            files = node_outputs.get(output_kind) or []
            if files:
                first = dict(files[0])
                first["node_id"] = node_id
                first["output_kind"] = output_kind
                return first

    raise ValueError(f"ComfyUI history has no output files for prompt id: {provider_job_id}")


def _asset_type_from_filename(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix in {".mp4", ".webm", ".mov", ".mkv", ".avi"}:
        return "video"
    if suffix in {".png", ".jpg", ".jpeg", ".webp"}:
        return "image"
    if suffix in {".wav", ".mp3", ".flac", ".ogg", ".m4a"}:
        return "audio"
    return "metadata"
