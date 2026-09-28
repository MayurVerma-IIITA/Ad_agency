from __future__ import annotations

from fastapi import FastAPI, HTTPException

from backend.config import get_settings
from backend.jobs import JobManager
from backend.models import JobRecord, VideoGenerationRequest
from backend.providers import build_video_provider

settings = get_settings()
provider = build_video_provider(settings)
jobs = JobManager(provider)

app = FastAPI(title="AI Ad Agency API")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate/video", response_model=JobRecord)
async def generate_video(request: VideoGenerationRequest) -> JobRecord:
    return await jobs.submit_video(request)


@app.get("/jobs/{job_id}", response_model=JobRecord)
async def get_job(job_id: str) -> JobRecord:
    job = await jobs.refresh_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job
