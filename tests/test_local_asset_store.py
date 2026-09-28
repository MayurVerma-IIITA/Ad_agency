from __future__ import annotations

from pathlib import Path

from backend.models import AssetRecord
from backend.storage import LocalAssetStore


def test_save_bytes_writes_file_under_asset_directory(tmp_path) -> None:
    store = LocalAssetStore(tmp_path)
    asset = AssetRecord(
        type="video",
        file_path=Path("comfyui/output/ad.mp4"),
        provider="wan",
        model="wan_test",
        prompt="ad",
    )

    stored = store.save_bytes(asset, "../ad.mp4", b"video bytes")

    assert stored.file_path == tmp_path / asset.asset_id / "ad.mp4"
    assert stored.file_path.read_bytes() == b"video bytes"
