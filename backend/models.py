from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class VideoMode(StrEnum):
    TEXT_TO_VIDEO = "text_to_video"
    IMAGE_TO_VIDEO = "image_to_video"


class CommercialStatus(StrEnum):
    APPROVED = "approved"
    CONDITIONAL = "conditional"
    RESEARCH_ONLY = "research_only"
    UNKNOWN = "unknown"


class ModelRegistryEntry(BaseModel):
    model_id: str
    name: str
    provider: str
    type: Literal["video", "image", "audio", "editing"]
    capabilities: list[str]
    license: str
    commercial_status: CommercialStatus
    enabled: bool = True
    notes: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class VideoGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1)
    negative_prompt: str = ""
    duration: int = Field(default=5, ge=1, le=30)
    width: int = Field(default=720, ge=256)
    height: int = Field(default=1280, ge=256)
    fps: int = Field(default=24, ge=1, le=60)
    mode: VideoMode = VideoMode.TEXT_TO_VIDEO
    model: str = "auto"
    commercial_use: bool = False
    image_asset_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class JobRecord(BaseModel):
    job_id: str = Field(default_factory=lambda: f"job_{uuid4().hex}")
    status: JobStatus = JobStatus.QUEUED
    request: VideoGenerationRequest
    provider_job_id: str | None = None
    asset_id: str | None = None
    error: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AssetRecord(BaseModel):
    asset_id: str = Field(default_factory=lambda: f"asset_{uuid4().hex}")
    type: Literal["video", "image", "audio", "metadata"]
    file_path: Path
    provider: str
    model: str
    prompt: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    license: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
