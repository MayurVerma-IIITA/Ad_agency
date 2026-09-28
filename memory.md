# Project Memory

## Durable Context

The project is an AI advertising production platform controlled through MCP by ChatGPT and Claude.

The long-term platform should generate images, videos, voiceovers, music, captions, edits, variations, and full advertising campaigns. The immediate focus is much smaller: prove a Wan 2.2 + ComfyUI video-generation vertical slice.

## Key Principles

- Keep the MCP interface model-agnostic.
- Keep model-specific logic isolated in providers.
- Use asynchronous jobs for long-running generation.
- Every generated output should become an asset with metadata.
- Track model license and commercial-use status explicitly.
- Do not assume free GPU infrastructure is permanent.
- Do not expose arbitrary shell execution through MCP tools.

## Technical Decisions

- Python is the initial backend language.
- FastAPI is the planned HTTP API layer.
- ComfyUI is the planned workflow execution layer.
- FFmpeg is the planned deterministic editing layer.
- Local filesystem storage is acceptable for MVP assets.
- PostgreSQL, Redis, object storage, and Kubernetes are deferred.

## Assumptions

- The local machine is primarily for development and orchestration.
- Heavy video inference will initially run on a free or temporary GPU environment.
- The first real provider implementation will target Wan through ComfyUI.
- A mocked or placeholder provider path is acceptable until ComfyUI is reachable.

## User Preferences

- Build one verified milestone at a time.
- Avoid over-engineering the full agency platform before the first video pipeline works.
