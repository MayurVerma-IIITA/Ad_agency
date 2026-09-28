# AI Ad Agency MCP

Model-agnostic advertising production infrastructure controlled through MCP.

The immediate goal is intentionally narrow: build a working video-generation vertical slice that can later be exposed to ChatGPT and Claude through MCP.

## Current Scope

This repository starts with:

- A minimal backend shape for asynchronous video generation jobs
- A `VideoProvider` interface
- A `WanProvider` adapter that keeps Wan/ComfyUI details isolated
- Local filesystem asset storage
- A placeholder MCP server package
- Durable project notes in `state.md` and `memory.md`

The first real production milestone is:

```text
prompt -> Agency MCP -> VideoProvider -> ComfyUI -> Wan 2.2 -> MP4
```

## Quick Start

Create a virtual environment, then install development dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Run tests:

```powershell
pytest
```

Run the API:

```powershell
uvicorn backend.api.main:app --reload
```

Run the mock ComfyUI service in a second terminal:

```powershell
uvicorn scripts.mock_comfyui:app --port 8188 --reload
```

The mock service is only for exercising API/job orchestration before a real GPU-backed ComfyUI endpoint is available.

For local smoke testing without a real Wan workflow, set:

```powershell
$env:WAN_WORKFLOW_PATH = "./workflows/video/mock-video.json"
uvicorn backend.api.main:app --reload
```

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

The initial implementation defaults to local asset storage under `./data/assets`.

To point the backend at a real exported ComfyUI workflow, set:

```powershell
WAN_WORKFLOW_PATH=./workflows/video/wan-text-to-video.json
```

## Roadmap

See [docs/ai-ad-agency-build-plan.md](docs/ai-ad-agency-build-plan.md).
