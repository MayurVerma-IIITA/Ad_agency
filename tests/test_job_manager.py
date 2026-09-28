from __future__ import annotations

from pathlib import Path

import pytest

from backend.jobs import JobManager
from backend.models import AssetRecord, JobRecord, JobStatus, VideoGenerationRequest
from backend.providers import VideoProvider


class FakeVideoProvider(VideoProvider):
    name = "fake"

    async def generate_text_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        return JobRecord(status=JobStatus.RUNNING, request=request, provider_job_id="provider_123")

    async def generate_image_to_video(self, request: VideoGenerationRequest) -> JobRecord:
        return JobRecord(status=JobStatus.RUNNING, request=request, provider_job_id="provider_456")

    async def get_status(self, provider_job_id: str) -> JobRecord:
        return JobRecord(
            status=JobStatus.COMPLETED,
            request=VideoGenerationRequest(prompt="status"),
            provider_job_id=provider_job_id,
            asset_id="asset_123",
        )

    async def get_result(self, provider_job_id: str) -> AssetRecord:
        return AssetRecord(
            type="video",
            file_path=Path("comfyui/output/mock-output.mp4"),
            provider=self.name,
            model="fake",
            prompt="cinematic perfume ad",
            parameters={"provider_job_id": provider_job_id},
        )


@pytest.mark.asyncio
async def test_submit_video_tracks_provider_job() -> None:
    manager = JobManager(FakeVideoProvider())

    job = await manager.submit_video(VideoGenerationRequest(prompt="cinematic perfume ad"))

    assert job.status == JobStatus.RUNNING
    assert job.provider_job_id == "provider_123"


@pytest.mark.asyncio
async def test_refresh_job_updates_completed_status() -> None:
    manager = JobManager(FakeVideoProvider())
    job = await manager.submit_video(VideoGenerationRequest(prompt="cinematic perfume ad"))

    refreshed = await manager.refresh_job(job.job_id)

    assert refreshed is not None
    assert refreshed.status == JobStatus.COMPLETED
    assert refreshed.asset_id is not None


@pytest.mark.asyncio
async def test_refresh_job_registers_completed_asset() -> None:
    manager = JobManager(FakeVideoProvider())
    job = await manager.submit_video(VideoGenerationRequest(prompt="cinematic perfume ad"))

    refreshed = await manager.refresh_job(job.job_id)

    assert refreshed is not None
    assert refreshed.asset_id is not None
    asset = await manager.get_asset(refreshed.asset_id)
    assert asset is not None
    assert asset.type == "video"
    assert asset.file_path == Path("comfyui/output/mock-output.mp4")


@pytest.mark.asyncio
async def test_refresh_job_does_not_duplicate_asset() -> None:
    manager = JobManager(FakeVideoProvider())
    job = await manager.submit_video(VideoGenerationRequest(prompt="cinematic perfume ad"))

    first = await manager.refresh_job(job.job_id)
    second = await manager.refresh_job(job.job_id)

    assert first is not None
    assert second is not None
    assert first.asset_id == second.asset_id
    assert len(await manager.list_assets()) == 1
