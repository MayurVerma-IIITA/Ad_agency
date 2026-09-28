from __future__ import annotations

from typing import Any

import httpx


class ComfyUIClient:
    """Thin ComfyUI HTTP client.

    This class intentionally knows about ComfyUI endpoints, while provider and
    job code only depend on higher-level generation concepts.
    """

    def __init__(
        self,
        base_url: str,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.transport = transport

    async def submit_prompt(self, workflow: dict[str, Any]) -> str:
        async with httpx.AsyncClient(timeout=30, transport=self.transport) as client:
            response = await client.post(f"{self.base_url}/prompt", json={"prompt": workflow})
            response.raise_for_status()
            data = response.json()
        prompt_id = data.get("prompt_id")
        if not prompt_id:
            raise ValueError("ComfyUI response did not include prompt_id")
        return str(prompt_id)

    async def get_history(self, prompt_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30, transport=self.transport) as client:
            response = await client.get(f"{self.base_url}/history/{prompt_id}")
            response.raise_for_status()
            return response.json()
