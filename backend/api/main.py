from __future__ import annotations

from fastapi import FastAPI, HTTPException

from backend.config import get_settings
from backend.jobs import JobManager
from backend.model_registry import ModelRegistry
from backend.models import AssetRecord, JobRecord, ModelRegistryEntry, VideoGenerationRequest
from backend.providers import build_video_provider

settings = get_settings()
provider = build_video_provider(settings)
jobs = JobManager(provider)
model_registry = ModelRegistry.from_file(settings.model_registry_path)

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


@app.get("/assets", response_model=list[AssetRecord])
async def list_assets() -> list[AssetRecord]:
    return await jobs.list_assets()


@app.get("/assets/{asset_id}", response_model=AssetRecord)
async def get_asset(asset_id: str) -> AssetRecord:
    asset = await jobs.get_asset(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    return asset


@app.get("/models", response_model=list[ModelRegistryEntry])
async def list_models() -> list[ModelRegistryEntry]:
    return model_registry.list()
