# Project State

## Status

Started the minimal repository scaffold for the AI Ad Agency MCP project.

## Completed

- Saved the comprehensive build plan to `docs/ai-ad-agency-build-plan.md`.
- Created the first backend package layout.
- Added a `VideoProvider` interface for text-to-video, image-to-video, status, and result retrieval.
- Added an isolated `WanProvider` adapter placeholder for ComfyUI-backed Wan execution.
- Added an in-memory job manager suitable for early orchestration tests.
- Added local filesystem asset storage.
- Added API and MCP placeholder entrypoints.
- Added a local Python virtual environment and installed project dev dependencies.
- Verified the current job orchestration tests pass.
- Initialized a local Git repository.
- Added workflow JSON loading and provider construction from settings.
- Added a mock ComfyUI service for local API smoke testing.
- Added ComfyUI client tests and a mock video workflow.
- Verified mock API flow: submit video job, receive provider job ID, refresh status to completed.
- Added in-memory asset catalog support to the job manager.
- Added API endpoints to list and fetch asset records.
- Added Wan provider output parsing from ComfyUI history into `AssetRecord`.
- Verified mock API flow through asset lookup.
- Preserved original generation prompt and request parameters on completed asset records.
- Added a JSON model registry with license and commercial-use metadata.
- Added model selection checks that reject unknown/research-only models for commercial requests.
- Added `GET /models` for registry inspection.

## In Progress

- First vertical slice architecture:
  - API receives a video generation request.
  - Job manager tracks async status.
  - Provider interface hides model-specific details.
  - Wan/ComfyUI wiring remains isolated.

## Pending

- Connect `WanProvider` to a real ComfyUI workflow JSON.
- Decide first free GPU execution environment.
- Add real ComfyUI `/prompt`, history, and output retrieval behavior.
- Expose the working flow through a real MCP server.
- Add integration tests once a ComfyUI endpoint is available.
- Download or copy real ComfyUI output files into durable local storage.
- Replace placeholder Wan license metadata after source/license verification.
- Add provider routing once there is more than one real model/provider.

## Blockers

- No running ComfyUI endpoint is configured yet.
- No Wan 2.2 workflow JSON has been added yet.

## Git / Deployment

- Local Git repository initialized.
- Remote `origin` is configured at `https://github.com/MayurVerma-IIITA/Ad_agency.git`.
- No deployment exists.

## Verification

- `.\.venv\Scripts\python.exe -m pytest` passes with 14 tests.
- Local smoke test passed using `scripts.mock_comfyui:app` and `workflows/video/mock-video.json`.
- Smoke test covered `POST /generate/video`, `GET /jobs/{job_id}`, and `GET /assets/{asset_id}`.
- API startup and `GET /models` smoke-tested against `models/registry.json`.
