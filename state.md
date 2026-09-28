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
- Added ComfyUI `/view` output download support.
- Added local asset storage writes under `data/assets/{asset_id}/`.
- Added request-driven ComfyUI workflow patching through `metadata.workflow_patches`.
- Added official Wan 2.2 5B TI2V UI workflow template.
- Added ComfyUI/Wan setup guide and workflow inspection script.
- Updated Wan registry metadata to Apache-2.0 / commercial approved, with production verification note.
- Added a Colab-oriented ComfyUI/Wan setup notebook and guide.

## In Progress

- First vertical slice architecture:
  - API receives a video generation request.
  - Job manager tracks async status.
  - Provider interface hides model-specific details.
  - Wan/ComfyUI wiring remains isolated.

## Pending

- Connect `WanProvider` to a real ComfyUI workflow JSON.
- Decide first free GPU execution environment.
- Export `workflows/video/wan-text-to-video-api.json` from ComfyUI after a successful manual generation.
- Run the Colab notebook or another GPU setup to produce the first manual Wan MP4.
- Add real ComfyUI `/prompt`, history, and output retrieval behavior.
- Expose the working flow through a real MCP server.
- Add integration tests once a ComfyUI endpoint is available.
- Validate the durable asset storage path against a real ComfyUI/Wan output file.
- Export a real Wan 2.2 ComfyUI workflow and identify patch paths for prompt, resolution, fps, and duration.
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

- `.\.venv\Scripts\python.exe -m pytest` passes with 21 tests.
- Local smoke test passed using `scripts.mock_comfyui:app` and `workflows/video/mock-video.json`.
- Smoke test covered `POST /generate/video`, `GET /jobs/{job_id}`, and `GET /assets/{asset_id}`.
- API startup and `GET /models` smoke-tested against `models/registry.json`.
- Mock API smoke test verified `mock-output.mp4` was written under `data/assets/{asset_id}/`.
- `.\.venv\Scripts\python.exe scripts\inspect_workflow.py workflows\video\wan-text-to-video-ui.json` succeeds.
