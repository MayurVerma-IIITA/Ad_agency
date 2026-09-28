from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from backend.comfy.client import ComfyUIClient
from backend.models import AssetRecord, JobRecord, JobStatus, VideoGenerationRequest
from backend.providers.base import VideoProvider


class WanProvider(VideoProvider):
    """Wan video provider backed by ComfyUI workflows.

    The workflow translation is deliberately isolated here so the API, MCP
    tools, and job manager do not become Wan-specific.
    """

    name = "wan"

    def __init__(self, comfyui: ComfyUIClient, workflow_template: dict[str, Any] | None = None) -> None:
        self.comfyui = comfyui
        self.workflow_template = workflow_template or {}

    async def generate_text_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        workflow = self._build_workflow(request)
        provider_job_id = await self.comfyui.submit_prompt(workflow)
        return JobRecord(
            status=JobStatus.RUNNING,
            request=request,
            provider_job_id=provider_job_id,
        )

    async def generate_image_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        if not request.image_asset_id:
            raise ValueError("image_asset_id is required for image-to-video generation")
        workflow = self._build_workflow(request)
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

    async def get_result(self, provider_job_id: str) -> AssetRecord:
        raise NotImplementedError("ComfyUI output download mapping is pending workflow integration")

    def _build_workflow(self, request: VideoGenerationRequest) -> dict[str, Any]:
        if not self.workflow_template:
            raise ValueError("Wan workflow template is not configured")

        workflow = dict(self.workflow_template)
        workflow["_agency_request"] = request.model_dump(mode="json")
        return workflow
