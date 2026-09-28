from __future__ import annotations

from abc import ABC, abstractmethod

from backend.models import AssetRecord, JobRecord, VideoGenerationRequest


class VideoProvider(ABC):
    """Model-agnostic contract for video generation backends."""

    name: str

    @abstractmethod
    async def generate_text_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        """Submit a text-to-video generation job."""

    @abstractmethod
    async def generate_image_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        """Submit an image-to-video generation job."""

    @abstractmethod
    async def get_status(self, provider_job_id: str) -> JobRecord:
        """Fetch provider-level job status."""

    @abstractmethod
    async def get_result(self, provider_job_id: str, request: VideoGenerationRequest) -> AssetRecord:
        """Fetch the completed provider result as an asset record."""
