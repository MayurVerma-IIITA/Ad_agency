from __future__ import annotations

import httpx
import pytest

from backend.comfy.client import ComfyUIClient


@pytest.mark.asyncio
async def test_submit_prompt_returns_prompt_id() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/prompt"
        assert request.method == "POST"
        return httpx.Response(200, json={"prompt_id": "prompt_123"})

    client = ComfyUIClient("http://testserver", transport=httpx.MockTransport(handler))

    prompt_id = await client.submit_prompt({"1": {"class_type": "MockNode"}})

    assert prompt_id == "prompt_123"


@pytest.mark.asyncio
async def test_submit_prompt_rejects_missing_prompt_id() -> None:
    client = ComfyUIClient(
        "http://testserver",
        transport=httpx.MockTransport(lambda request: httpx.Response(200, json={})),
    )

    with pytest.raises(ValueError):
        await client.submit_prompt({"1": {"class_type": "MockNode"}})


@pytest.mark.asyncio
async def test_get_history_returns_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/history/prompt_123"
        return httpx.Response(200, json={"prompt_123": {"outputs": {}}})

    client = ComfyUIClient("http://testserver", transport=httpx.MockTransport(handler))

    history = await client.get_history("prompt_123")

    assert "prompt_123" in history
