from __future__ import annotations

from datetime import datetime, timezone

from backend.models import JobRecord, JobStatus, VideoGenerationRequest, VideoMode
from backend.providers.base import VideoProvider


class JobManager:
    def __init__(self, video_provider: VideoProvider) -> None:
        self.video_provider = video_provider
        self._jobs: dict[str, JobRecord] = {}

    async def submit_video(self, request: VideoGenerationRequest) -> JobRecord:
        queued = JobRecord(request=request)
        self._jobs[queued.job_id] = queued

        try:
            if request.mode == VideoMode.IMAGE_TO_VIDEO:
                provider_job = await self.video_provider.generate_image_to_video(request)
            else:
                provider_job = await self.video_provider.generate_text_to_video(request)
        except Exception as exc:
            return self._update(
                queued.job_id,
                status=JobStatus.FAILED,
                error=str(exc),
            )

        return self._update(
            queued.job_id,
            status=provider_job.status,
            provider_job_id=provider_job.provider_job_id,
        )

    async def get_job(self, job_id: str) -> JobRecord | None:
        return self._jobs.get(job_id)

    async def refresh_job(self, job_id: str) -> JobRecord | None:
        job = self._jobs.get(job_id)
        if not job or not job.provider_job_id:
            return job

        provider_status = await self.video_provider.get_status(job.provider_job_id)
        return self._update(job_id, status=provider_status.status, asset_id=provider_status.asset_id)

    def _update(self, job_id: str, **changes: object) -> JobRecord:
        job = self._jobs[job_id]
        updated = job.model_copy(update={**changes, "updated_at": datetime.now(timezone.utc)})
        self._jobs[job_id] = updated
        return updated
