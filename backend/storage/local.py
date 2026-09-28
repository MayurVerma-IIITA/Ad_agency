from __future__ import annotations

from pathlib import Path

from backend.models import AssetRecord


class LocalAssetStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def path_for(self, asset: AssetRecord) -> Path:
        asset_dir = self.root / asset.asset_id
        asset_dir.mkdir(parents=True, exist_ok=True)
        return asset_dir / asset.file_path.name
