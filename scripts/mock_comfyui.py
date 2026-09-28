from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel


class PromptRequest(BaseModel):
    prompt: dict


app = FastAPI(title="Mock ComfyUI")
_jobs: dict[str, dict] = {}


@app.get("/system_stats")
async def system_stats() -> dict:
    return {"system": {"os": "mock"}, "devices": []}


@app.post("/prompt")
async def prompt(request: PromptRequest) -> dict[str, str]:
    prompt_id = uuid4().hex
    _jobs[prompt_id] = {
        "prompt": request.prompt,
        "outputs": {
            "mock_save_video": {
                "gifs": [
                    {
                        "filename": "mock-output.mp4",
                        "subfolder": "",
                        "type": "output",
                    }
                ]
            }
        },
    }
    return {"prompt_id": prompt_id}


@app.get("/history/{prompt_id}")
async def history(prompt_id: str) -> dict:
    job = _jobs.get(prompt_id)
    if not job:
        raise HTTPException(status_code=404, detail="prompt not found")
    return {prompt_id: job}


@app.get("/view")
async def view(filename: str, subfolder: str = "", type: str = "output") -> Response:
    if filename != "mock-output.mp4" or type != "output":
        raise HTTPException(status_code=404, detail="output not found")
    return Response(content=b"mock mp4 bytes", media_type="video/mp4")
