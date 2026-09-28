from __future__ import annotations

import json
from pathlib import Path

from backend.models import CommercialStatus, ModelRegistryEntry, VideoGenerationRequest


class ModelRegistry:
    def __init__(self, entries: list[ModelRegistryEntry]) -> None:
        self._entries = {entry.model_id: entry for entry in entries}

    @classmethod
    def from_file(cls, path: Path) -> "ModelRegistry":
        if not path.exists():
            raise FileNotFoundError(f"Model registry not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            raw = json.load(file)

        if not isinstance(raw, dict) or not isinstance(raw.get("models"), list):
            raise ValueError("Model registry must contain a top-level 'models' list")

        return cls([ModelRegistryEntry.model_validate(entry) for entry in raw["models"]])

    def list(self) -> list[ModelRegistryEntry]:
        return list(self._entries.values())

    def get(self, model_id: str) -> ModelRegistryEntry | None:
        return self._entries.get(model_id)

    def select_video_model(self, request: VideoGenerationRequest, provider: str) -> ModelRegistryEntry:
        if request.model != "auto":
            entry = self.get(request.model)
            if not entry:
                raise ValueError(f"Unknown model: {request.model}")
            self._validate_video_entry(entry, request, provider)
            return entry

        candidates = [
            entry
            for entry in self._entries.values()
            if entry.enabled
            and entry.provider == provider
            and entry.type == "video"
            and request.mode.value in entry.capabilities
        ]

        if request.commercial_use:
            candidates = [
                entry
                for entry in candidates
                if entry.commercial_status in {CommercialStatus.APPROVED, CommercialStatus.CONDITIONAL}
            ]

        if not candidates:
            raise ValueError(
                f"No enabled {provider} video model supports {request.mode.value}"
                + (" for commercial use" if request.commercial_use else "")
            )

        return candidates[0]

    def _validate_video_entry(
        self,
        entry: ModelRegistryEntry,
        request: VideoGenerationRequest,
        provider: str,
    ) -> None:
        if not entry.enabled:
            raise ValueError(f"Model is disabled: {entry.model_id}")
        if entry.provider != provider:
            raise ValueError(f"Model {entry.model_id} is not served by provider {provider}")
        if entry.type != "video":
            raise ValueError(f"Model {entry.model_id} is not a video model")
        if request.mode.value not in entry.capabilities:
            raise ValueError(f"Model {entry.model_id} does not support {request.mode.value}")
        if request.commercial_use and entry.commercial_status not in {
            CommercialStatus.APPROVED,
            CommercialStatus.CONDITIONAL,
        }:
            raise ValueError(f"Model {entry.model_id} is not approved for commercial use")
