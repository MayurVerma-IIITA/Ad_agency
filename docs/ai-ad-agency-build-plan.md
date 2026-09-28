Below is a **Codex-ready technical specification/roadmap**. It deliberately separates the MVP from the eventual AI-agency platform so Codex does not over-engineer the first iteration.

# AI Ad Agency MCP — Comprehensive Build Plan

## 1. Project Vision

Build a **model-agnostic AI advertising production platform** that can be controlled through **ChatGPT and Claude using MCP**.

The long-term goal is to create an AI-powered advertising agency capable of taking a natural-language client brief and automatically producing advertising creatives:

* Images
* Short videos
* Product commercials
* Social-media ads
* UGC-style ads
* AI-character videos
* Voiceovers
* Music/SFX
* Captions
* Video editing
* Multiple aspect ratios
* Multiple creative variations
* Final downloadable/exportable advertisements

The platform should initially cost **₹0 in API/model inference fees** by prioritizing open-source models and free/temporary GPU resources.

However, the architecture must be designed so that paid GPU infrastructure and additional commercial models/providers can be added later without changing the MCP interface.

---

# 2. Core Design Philosophy

The system must be:

1. **Model agnostic**
2. **Provider agnostic**
3. **MCP-first**
4. **Automation-first**
5. **Commercial-use conscious**
6. **Open-source friendly**
7. **Replaceable at every layer**
8. **Scalable from personal experimentation to agency infrastructure**

Do NOT tightly couple the system to one model such as Seedance, Wan, LTX, Hunyuan, etc.

The MCP should expose capabilities such as:

```text
generate_video()
generate_image()
image_to_video()
video_to_video()
generate_voice()
generate_music()
edit_video()
add_captions()
create_ad()
create_campaign()
```

rather than model-specific functions such as:

```text
generate_wan_video()
generate_ltx_video()
```

The backend decides which model/provider should execute the task.

---

# 3. Target Architecture

```text
                         ┌──────────────────────┐
                         │      ChatGPT         │
                         └──────────┬───────────┘
                                    │
                         ┌──────────▼───────────┐
                         │       Claude         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Agency MCP      │
                         │                      │
                         │ Natural-language     │
                         │ production tools     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Workflow / Job      │
                         │      Router           │
                         └──────────┬───────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               │                    │                    │
               ▼                    ▼                    ▼
       ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
       │ Image Engine │     │ Video Engine │     │ Audio Engine │
       └──────────────┘     └──────────────┘     └──────────────┘
               │                    │                    │
               ▼                    ▼                    ▼
          Open Models          Open Models          Open Models
               │                    │                    │
               └────────────────────┼────────────────────┘
                                    ▼
                             ┌──────────────┐
                             │   ComfyUI    │
                             │  Workflows   │
                             └──────┬───────┘
                                    │
                                    ▼
                              GPU Worker(s)
                                    │
                                    ▼
                             ┌──────────────┐
                             │    FFmpeg    │
                             │ Video Editing│
                             └──────┬───────┘
                                    │
                                    ▼
                              Final Assets
```

---

# 4. Phase 1 — Video Generation MVP

The first objective is NOT to build the entire agency.

The first objective is:

> Get a reliable open-source video-generation pipeline working on free/temporary GPU infrastructure.

Initial stack:

```text
ComfyUI
+
Wan 2.2 TI2V-5B
+
Free GPU
```

The initial model should support:

* Text → Video
* Image → Video

The first successful milestone should be:

```text
Prompt
   ↓
Wan 2.2
   ↓
5–10 second video
   ↓
MP4
```

Example:

```text
Generate a cinematic 5-second perfume advertisement.
A luxury perfume bottle stands on a black reflective
surface, dramatic lighting, slow camera movement,
premium commercial aesthetic.
```

The system should produce an actual MP4.

---

# 5. Phase 1.1 — ComfyUI

Use ComfyUI as the model execution/workflow layer.

Reasons:

* Open source
* Node-based workflow system
* Large model ecosystem
* Video support
* Image generation support
* Audio support
* Extensible
* Easy to replace models
* Can expose workflows through APIs
* Compatible with MCP integration

Do NOT implement video-generation inference directly inside the MCP.

The MCP should orchestrate ComfyUI.

Architecture:

```text
MCP
 ↓
ComfyUI API
 ↓
Workflow
 ↓
Model
 ↓
GPU
```

---

# 6. Phase 1.2 — GPU Strategy

The developer's local laptop should NOT be required to run large video models.

The laptop is primarily:

* Development machine
* MCP client
* Code editor
* Git environment
* Management/control interface

Heavy inference should initially run on free/temporary GPU infrastructure.

Potential development environments:

* Google Colab
* Kaggle
* Hugging Face Spaces/ZeroGPU
* Other legitimate free GPU environments

The system must NOT depend permanently on one provider.

Create a GPU abstraction:

```text
GPUProvider
    ├── ColabProvider
    ├── KaggleProvider
    ├── HuggingFaceProvider
    └── FuturePaidGPUProvider
```

The implementation can initially support only one provider.

Do not over-engineer this abstraction before the first working pipeline exists.

---

# 7. Phase 2 — ComfyUI API Integration

Once Wan works manually in ComfyUI, expose the workflow programmatically.

The backend should be able to:

1. Submit a workflow
2. Generate a job ID
3. Track job status
4. Detect completion
5. Retrieve output files
6. Return metadata
7. Handle errors

Conceptual API:

```text
POST /generate/video
```

Request:

```json
{
  "prompt": "cinematic perfume commercial",
  "negative_prompt": "",
  "duration": 5,
  "width": 720,
  "height": 1280,
  "fps": 24,
  "mode": "text_to_video"
}
```

Response:

```json
{
  "job_id": "job_123",
  "status": "queued"
}
```

Status:

```text
GET /jobs/job_123
```

Response:

```json
{
  "job_id": "job_123",
  "status": "completed",
  "asset_id": "asset_456"
}
```

---

# 8. Phase 3 — Build the Custom Agency MCP

Once video generation works independently, create the custom MCP.

The MCP should NOT contain the actual ML inference logic.

Its responsibility is:

```text
LLM
 ↓
MCP
 ↓
Workflow service
 ↓
ComfyUI
 ↓
GPU
```

The MCP becomes the standardized interface between AI assistants and the production system.

---

# 9. MCP Tool Design

Initial tools:

## Video

```text
generate_video()
image_to_video()
video_to_video()
extend_video()
```

## Images

```text
generate_image()
edit_image()
upscale_image()
```

## Audio

```text
generate_voice()
generate_music()
generate_sfx()
```

## Editing

```text
trim_video()
join_clips()
resize_video()
add_audio()
add_voiceover()
add_captions()
add_logo()
```

## Jobs

```text
get_job_status()
cancel_job()
list_jobs()
```

## Assets

```text
list_assets()
get_asset()
download_asset()
delete_asset()
```

Later:

```text
create_ad()
create_campaign()
create_storyboard()
create_shot_list()
```

---

# 10. Model Router

The MCP should not care which model executes a request.

Create a model-selection layer.

Example:

```text
generate_video()
        ↓
VideoRouter
        ↓
┌────────────────────────────┐
│ Determine requirements     │
│                            │
│ text/image/video input     │
│ duration                   │
│ resolution                 │
│ style                      │
│ quality                    │
│ available GPU              │
│ model license              │
└─────────────┬──────────────┘
              ↓
       Select model
```

Potential models:

```text
Wan
LTX
Hunyuan
Future open-source models
Future commercial providers
```

Do not hard-code one model.

Example:

```json
{
  "model": "auto"
}
```

The router determines the appropriate backend.

---

# 11. Model Registry

Create a model registry.

Conceptually:

```json
{
  "wan_t2v": {
    "type": "video",
    "capabilities": [
      "text_to_video"
    ],
    "license": "Apache-2.0",
    "enabled": true
  },

  "wan_i2v": {
    "type": "video",
    "capabilities": [
      "image_to_video"
    ],
    "license": "Apache-2.0",
    "enabled": true
  }
}
```

The registry should eventually contain:

* Model name
* Version
* Capabilities
* VRAM requirements
* Resolution
* Maximum practical duration
* License
* Commercial-use restrictions
* Input formats
* Output formats
* Provider
* Availability
* Performance metadata

This allows the router to make informed choices.

---

# 12. Commercial Licensing Layer

Commercial licensing is a first-class requirement.

Do NOT assume:

```text
Open source = commercially safe
```

For every model, record:

```text
Model
License
Commercial use?
Revenue restrictions?
Geographical restrictions?
Redistribution restrictions?
Attribution requirements?
Generated-output restrictions?
Trademark restrictions?
```

The platform should maintain a `model_license` metadata record.

Example:

```text
Model: Wan
License: Apache-2.0
Commercial use: generally permitted under license
Additional review: required for actual client deployment
```

For models with restrictions, mark them clearly:

```text
commercial_status:
    approved
    conditional
    research_only
    unknown
```

The system should be able to prevent accidental use of a research-only model for client production.

---

# 13. Phase 4 — Image Generation

Add image generation through ComfyUI.

Use cases:

* Product photography
* Product backgrounds
* Characters
* Storyboards
* Ad creatives
* Social media posts
* Thumbnail generation
* Reference images for video generation

Important workflow:

```text
Client product image
        ↓
Image editing
        ↓
Commercial scene
        ↓
Image-to-video
```

This is particularly important for advertising.

---

# 14. Phase 5 — Ad Production Pipeline

Eventually introduce a high-level:

```text
create_ad()
```

tool.

Input:

```json
{
  "brand": "Example Perfume",
  "product": "Luxury perfume",
  "target_audience": "Young professionals",
  "platform": "Instagram",
  "duration": 30,
  "aspect_ratio": "9:16",
  "style": "premium cinematic"
}
```

The system should automatically generate:

```text
Campaign concept
        ↓
Creative direction
        ↓
Script
        ↓
Storyboard
        ↓
Shot list
        ↓
Reference images
        ↓
Video clips
        ↓
Voiceover
        ↓
Music
        ↓
Editing
        ↓
Captions
        ↓
Final video
```

---

# 15. Shot-Based Video Generation

Do NOT attempt to create long advertisements in one model generation.

Instead, represent the advertisement as shots.

Example:

```text
AD
│
├── Shot 1
│   ├── Prompt
│   ├── Image
│   ├── Video
│   ├── Duration
│   └── Audio
│
├── Shot 2
│
├── Shot 3
│
├── Shot 4
│
└── Shot 5
```

Each shot should have:

```json
{
  "shot_id": "shot_001",
  "duration": 5,
  "prompt": "...",
  "camera": "...",
  "lighting": "...",
  "style": "...",
  "transition": "...",
  "voiceover": "...",
  "music": "..."
}
```

Then combine the shots with FFmpeg.

---

# 16. Consistency System

Advertising requires consistency.

The system should eventually maintain:

```text
Brand
 ├── Logo
 ├── Colors
 ├── Fonts
 ├── Product images
 ├── Product descriptions
 ├── Character references
 ├── Voice
 ├── Style
 └── Creative rules
```

For characters:

```text
Character Reference
        ↓
Shot 1
Shot 2
Shot 3
Shot 4
```

For products:

```text
Product Reference
        ↓
All generated scenes
```

This becomes critical for commercial-quality output.

---

# 17. Video Editing Layer

Use FFmpeg as the initial deterministic editing engine.

Capabilities:

```text
trim
concat
resize
crop
scale
fps conversion
audio mixing
voiceover
music
subtitles
watermarks
logos
fade
volume
format conversion
```

Example:

```text
5 generated clips
      ↓
FFmpeg
      ↓
30-second advertisement
      ↓
1080x1920
      ↓
H.264 MP4
```

Later, AI-based editing can be added separately.

---

# 18. Audio Pipeline

Add an audio abstraction:

```text
AudioRouter
   ├── TTS
   ├── Voice cloning
   ├── Music
   └── SFX
```

The system should support:

```text
Script
 ↓
Voiceover
 ↓
Music
 ↓
SFX
 ↓
Audio mixing
 ↓
Final video
```

Commercial licensing must also be checked for generated music, voices, and sound effects.

---

# 19. Caption Pipeline

The platform should automatically generate captions.

Pipeline:

```text
Voiceover
   ↓
Speech-to-text
   ↓
Subtitle timing
   ↓
SRT / ASS
   ↓
FFmpeg
   ↓
Burned captions
```

Support:

```text
Instagram
YouTube Shorts
TikTok
YouTube
LinkedIn
```

---

# 20. Aspect Ratio System

The same creative should eventually be exportable as:

```text
9:16
Instagram Reels
YouTube Shorts

1:1
Instagram feed

4:5
Instagram feed

16:9
YouTube / website

16:9
Traditional commercial
```

The system should store the master project separately from rendered exports.

---

# 21. Asset Management

Introduce an asset system.

Conceptually:

```text
Project
 ├── Brief
 ├── Script
 ├── Storyboard
 ├── Images
 ├── Videos
 ├── Audio
 ├── Captions
 ├── Versions
 └── Exports
```

Every generated asset should have:

```text
asset_id
project_id
type
model
model_version
prompt
parameters
license
created_at
file_path
metadata
```

This is essential for reproducibility.

---

# 22. Database

Eventually use PostgreSQL.

Potential tables:

```text
users
clients
projects
campaigns
briefs
shots
assets
generation_jobs
models
model_licenses
workflows
exports
providers
```

For the initial MVP, a lightweight database can be used.

Do not introduce PostgreSQL merely to generate the first video.

---

# 23. Job Queue

Video generation is asynchronous.

Never assume:

```text
request → immediate response
```

Use:

```text
request
 ↓
job
 ↓
queue
 ↓
GPU worker
 ↓
generation
 ↓
asset
```

Later architecture:

```text
MCP
 ↓
API
 ↓
Redis
 ↓
Worker
 ↓
ComfyUI
 ↓
GPU
```

The MCP should return a job ID for long-running operations.

---

# 24. Storage

Initial:

```text
Local filesystem
```

Later:

```text
S3-compatible object storage
```

Potential structure:

```text
/projects/{project_id}/
    /brief/
    /images/
    /videos/
    /audio/
    /renders/
    /exports/
```

Never rely on temporary GPU storage as permanent asset storage.

---

# 25. Remote MCP Architecture

For local development:

```text
Claude
 ↓
local MCP
 ↓
local ComfyUI
```

Eventually:

```text
ChatGPT
       \
        → HTTPS → Agency MCP → Workflow API → GPU
       /
Claude
```

The MCP server should be remotely accessible and authenticated.

Use:

```text
HTTPS
authentication
authorization
rate limits
job isolation
secure file access
```

Do not expose ComfyUI directly to the public Internet.

---

# 26. Security Requirements

The eventual system handles:

* Client products
* Brand assets
* Potentially private videos
* Voice recordings
* Commercial campaigns

Therefore:

```text
Authentication
Authorization
Project isolation
Secure asset URLs
Input validation
Prompt validation
File-type validation
File-size limits
Rate limiting
Secrets management
```

must eventually be implemented.

---

# 27. MCP Security Principle

Never allow an LLM to execute arbitrary shell commands.

Bad:

```text
execute_shell(command)
```

Prefer:

```text
generate_video(...)
render_video(...)
list_assets(...)
delete_asset(asset_id)
```

Every capability should be explicitly exposed.

---

# 28. Observability

Every generation should be traceable.

Record:

```text
request
model
workflow
parameters
GPU provider
job ID
duration
status
errors
output asset
```

Eventually add:

```text
generation cost
GPU time
failure rate
average generation time
model success rate
```

Even though the initial goal is ₹0, these metrics become essential when the agency scales.

---

# 29. Provider Abstraction

Design:

```text
InferenceProvider
       │
       ├── FreeGPUProvider
       ├── HuggingFaceProvider
       ├── ColabProvider
       ├── SelfHostedProvider
       └── PaidGPUProvider
```

Eventually:

```text
VideoProvider
       ├── LocalComfyUI
       ├── RemoteComfyUI
       ├── OpenSourceModel
       └── CommercialAPI
```

The MCP should not change when providers change.

---

# 30. Zero-Cost Strategy

Initial target:

```text
Software
    Open source

Models
    Open source

Inference
    Free GPU

Editing
    FFmpeg

MCP
    Open source/custom

Storage
    Local

Database
    Local

Development
    Local laptop
```

But explicitly distinguish:

### Development cost

Target:

```text
₹0
```

### Production cost

Not guaranteed to remain:

```text
₹0
```

Free GPU providers can impose:

* quotas
* session limits
* queue limits
* GPU availability limits
* acceptable-use restrictions
* commercial-use restrictions

Therefore, production infrastructure must eventually be replaceable.

---

# 31. Seedance Strategy

Do not make Seedance a dependency.

If a legitimate free/commercially usable access path becomes available, implement it as another provider:

```text
VideoRouter
    ├── Wan
    ├── LTX
    ├── Seedance
    ├── Hunyuan
    └── Future models
```

Never design the entire system around Seedance.

---

# 32. AI Agency Workflow

Eventually the primary interface should become:

```text
User:
"Create an Instagram ad for my perfume."
```

The LLM should determine that it needs to:

```text
1. Understand product
2. Define audience
3. Develop creative concept
4. Write script
5. Create storyboard
6. Generate shot prompts
7. Generate reference images
8. Generate videos
9. Generate voiceover
10. Generate music
11. Generate captions
12. Assemble video
13. Render multiple formats
14. Return final assets
```

The MCP executes the actual operations.

The LLM acts as:

```text
Creative Director
+
Production Planner
+
Workflow Orchestrator
```

The MCP acts as:

```text
Production Infrastructure
```

---

# 33. Example End-to-End Request

User:

> Create a 30-second Instagram Reel advertisement for my premium perfume.

LLM:

```text
create_ad()
```

System:

```text
Campaign
 ↓
Creative concept
 ↓
Script
 ↓
Storyboard
 ↓
5 shots
 ↓
Product reference
 ↓
Image generation
 ↓
Video generation
 ↓
Voice generation
 ↓
Music generation
 ↓
Caption generation
 ↓
FFmpeg
 ↓
9:16 MP4
```

Output:

```text
final_ad.mp4
thumbnail.jpg
caption.txt
script.txt
project.json
```

---

# 34. Versioning

Every generated result should be reproducible.

Store:

```text
prompt
negative_prompt
model
model_version
workflow
seed
resolution
fps
duration
parameters
input assets
```

Example:

```text
project_001
    version_001
    version_002
    version_003
```

This allows:

> "Regenerate shot 3 using the same settings but a different camera movement."

---

# 35. Development Roadmap

## Milestone 1 — Working Video Generator

Build:

```text
ComfyUI
+
Wan 2.2
+
Free GPU
```

Success criteria:

* Text → video works
* Image → video works
* MP4 produced
* Workflow saved
* Model configuration documented

---

## Milestone 2 — Programmatic Generation

Build:

```text
Python
 ↓
ComfyUI API
 ↓
Workflow
 ↓
MP4
```

Success criteria:

```text
POST request
 ↓
job ID
 ↓
status
 ↓
completed
 ↓
video file
```

---

## Milestone 3 — MCP

Build:

```text
Claude
 ↓
MCP
 ↓
ComfyUI
```

Tools:

```text
generate_video()
image_to_video()
get_job_status()
get_asset()
```

---

## Milestone 4 — ChatGPT Integration

Make the same MCP accessible remotely.

Target:

```text
ChatGPT
      \
       MCP
      /
Claude
```

Both should control the same backend.

---

## Milestone 5 — Image Generation

Add:

```text
generate_image()
edit_image()
upscale_image()
```

---

## Milestone 6 — Audio

Add:

```text
generate_voice()
generate_music()
generate_sfx()
```

---

## Milestone 7 — Editing

Add:

```text
trim_video()
concat_video()
add_audio()
add_captions()
resize_video()
render_ad()
```

---

## Milestone 8 — Ad Generator

Implement:

```text
create_ad()
```

with:

```text
brief
→ concept
→ script
→ storyboard
→ shots
→ generation
→ editing
→ export
```

---

## Milestone 9 — Campaign System

Implement:

```text
create_campaign()
```

Support:

```text
multiple ads
multiple variations
multiple platforms
multiple aspect ratios
A/B creative variants
```

---

## Milestone 10 — Agency Platform

Add:

```text
clients
projects
campaigns
brand kits
assets
approvals
versions
analytics
billing
```

This becomes the foundation of the eventual AI ad agency.

---

# 36. Recommended Technology Stack

Initial:

```text
Python
FastAPI
MCP SDK
ComfyUI
Wan 2.2
FFmpeg
Git
Docker
```

Later:

```text
PostgreSQL
Redis
Object Storage
GPU workers
Docker Compose
Kubernetes (only if actually required)
```

Do not introduce Kubernetes early.

---

# 37. Repository Structure

Suggested structure:

```text
ai-ad-agency/
│
├── mcp-server/
│   ├── tools/
│   ├── resources/
│   ├── prompts/
│   └── server.py
│
├── backend/
│   ├── api/
│   ├── services/
│   ├── routers/
│   ├── models/
│   ├── providers/
│   ├── jobs/
│   └── storage/
│
├── workflows/
│   ├── video/
│   ├── image/
│   ├── audio/
│   └── editing/
│
├── models/
│   └── registry.yaml
│
├── scripts/
│
├── tests/
│
├── docs/
│
├── docker/
│
├── .env.example
├── docker-compose.yml
├── README.md
└── LICENSE
```

---

# 38. Engineering Principles for Codex

Codex should follow these rules:

### Rule 1

Do not implement the entire platform at once.

Build one working vertical slice at a time.

### Rule 2

Every major component should have a clean interface.

### Rule 3

Keep model-specific code isolated.

Bad:

```text
business logic → Wan-specific code
```

Good:

```text
business logic
      ↓
VideoProvider interface
      ↓
WanProvider
```

### Rule 4

Never expose model-specific details unnecessarily to MCP clients.

### Rule 5

Long-running tasks must be asynchronous.

### Rule 6

Every generation produces an asset and metadata.

### Rule 7

Every model has explicit license metadata.

### Rule 8

Do not assume free infrastructure is permanent.

### Rule 9

Keep configuration in environment variables/config files.

### Rule 10

Write tests for provider interfaces and job orchestration.

---

# 39. First Coding Task for Codex

Do NOT start building the entire agency.

Start with:

## Task 1

Create a minimal repository.

```text
ai-ad-agency/
├── backend/
├── mcp-server/
├── workflows/
├── tests/
├── docs/
├── .env.example
├── README.md
└── docker-compose.yml
```

Then create a provider interface:

```python
class VideoProvider:
    async def generate_text_to_video(...):
        ...

    async def generate_image_to_video(...):
        ...

    async def get_status(...):
        ...

    async def get_result(...):
        ...
```

Then create:

```text
WanProvider
```

without putting Wan-specific logic throughout the application.

Then implement the ComfyUI integration.

---

# 40. Definition of Done for the First Version

The first version is successful when this works:

```text
ChatGPT / Claude
       ↓
generate_video(
    prompt="cinematic perfume advertisement"
)
       ↓
Agency MCP
       ↓
VideoProvider
       ↓
ComfyUI
       ↓
Wan 2.2
       ↓
Free GPU
       ↓
MP4
       ↓
MCP
       ↓
ChatGPT / Claude
```

The user should not need to manually open ComfyUI after the integration is complete.

---

# 41. Long-Term Vision

The final product should feel like:

> **"Give the AI a product and a marketing objective; the AI handles the creative production pipeline."**

For example:

```text
User
│
│ "Create 3 Instagram ads for this product."
│
▼
AI Creative Director
│
├── Research / brief
├── Creative concepts
├── Scripts
├── Storyboards
│
▼
Production Engine
│
├── Images
├── Videos
├── Voices
├── Music
├── SFX
│
▼
Post Production
│
├── Editing
├── Captions
├── Branding
├── Aspect ratios
│
▼
QA
│
├── Resolution
├── Audio
├── Duration
├── Brand consistency
└── Output format
│
▼
Final Deliverables
│
├── Ad 1
├── Ad 2
├── Ad 3
├── Thumbnails
├── Captions
└── Source metadata
```

The immediate objective, however, remains much smaller:

> **Get Wan 2.2 working through ComfyUI on free GPU infrastructure, then expose that working pipeline through a clean MCP interface.**

Everything else should be built on top of that verified foundation.

For Codex, I would give it **this document plus the explicit instruction: “Do not jump ahead to the full platform. Implement and verify one milestone at a time, starting with the Wan 2.2 + ComfyUI vertical slice.”**
