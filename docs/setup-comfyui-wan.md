# ComfyUI + Wan 2.2 Setup

This project is ready to call a GPU-backed ComfyUI server. The missing runtime piece is a working Wan 2.2 workflow exported in ComfyUI API format.

## What To Install

Use a GPU environment for ComfyUI. The local laptop can stay as the orchestrator.

Download the Wan 2.2 5B TI2V assets into the ComfyUI model folders:

```text
ComfyUI/
  models/
    diffusion_models/
      wan2.2_ti2v_5B_fp16.safetensors
    text_encoders/
      umt5_xxl_fp8_e4m3fn_scaled.safetensors
    vae/
      wan2.2_vae.safetensors
```

The UI workflow template in this repo is:

```text
workflows/video/wan-text-to-video-ui.json
```

Load that file in ComfyUI to test manually.

## Export API Format

The backend must submit ComfyUI API prompt JSON, not UI workflow JSON.

In ComfyUI:

1. Open settings.
2. Enable developer mode if needed.
3. Load `workflows/video/wan-text-to-video-ui.json`.
4. Generate one successful MP4 manually.
5. Use `Save (API Format)`.
6. Save the result as:

```text
workflows/video/wan-text-to-video-api.json
```

Then run:

```powershell
.\.venv\Scripts\python.exe scripts\inspect_workflow.py workflows\video\wan-text-to-video-api.json
```

Use the printed node IDs and inputs to create `metadata.workflow_patches` for request-specific values.

## Backend Smoke Test

Start ComfyUI on the GPU machine and expose only the ComfyUI API URL you intend to use.

Then run the backend locally:

```powershell
$env:COMFYUI_BASE_URL = "http://YOUR_COMFYUI_HOST:8188"
$env:WAN_WORKFLOW_PATH = "./workflows/video/wan-text-to-video-api.json"
.\.venv\Scripts\python.exe -m uvicorn backend.api.main:app --reload
```

Submit a request:

```powershell
$body = @{
  prompt = "cinematic 5-second perfume advertisement, luxury bottle on black reflective surface, dramatic lighting"
  negative_prompt = "low quality, blurry, distorted"
  width = 720
  height = 1280
  fps = 24
  duration = 5
  commercial_use = $true
  metadata = @{
    workflow_patches = @{
      "6.inputs.text" = "prompt"
      "7.inputs.text" = "negative_prompt"
    }
  }
} | ConvertTo-Json -Depth 10

$job = Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/generate/video" -ContentType "application/json" -Body $body
$job
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:8000/jobs/$($job.job_id)"
```

Adjust the workflow patch paths after inspecting the exported API workflow. The example paths above are likely for prompt nodes, but the exact API-format paths must be confirmed from your export.

## Security Note

Do not expose ComfyUI directly to the public internet for production use. For early testing, use a temporary trusted tunnel or private network, then close it after the run.
