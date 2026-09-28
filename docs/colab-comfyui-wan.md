# Colab Setup: ComfyUI + Wan 2.2 5B

Use this when your local machine does not have a CUDA/NVIDIA GPU.

## Goal

Run ComfyUI on a temporary Colab GPU, generate one Wan 2.2 video manually, then export the workflow in API format for the backend.

## Steps

1. Open Google Colab.
2. Create a new notebook.
3. Set runtime:
   - `Runtime` -> `Change runtime type`
   - Hardware accelerator: GPU
4. Copy the cells from:

```text
notebooks/comfyui_wan_colab.ipynb
```

or upload/open that notebook directly.

## Required Model Files

The notebook downloads:

```text
ComfyUI/models/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors
ComfyUI/models/text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors
ComfyUI/models/vae/wan2.2_vae.safetensors
```

These are large files. The first download can take a while.

## Manual ComfyUI Test

When ComfyUI opens:

1. Load this workflow:

```text
workflows/video/wan-text-to-video-ui.json
```

2. Use a simple prompt:

```text
cinematic 5-second perfume advertisement, luxury bottle on black reflective surface, dramatic lighting, slow camera movement, premium commercial aesthetic
```

3. Generate one MP4.
4. If it works, export:

```text
Save (API Format)
```

5. Save that exported file in this repo as:

```text
workflows/video/wan-text-to-video-api.json
```

## After Export

Run locally:

```powershell
.\.venv\Scripts\python.exe scripts\inspect_workflow.py workflows\video\wan-text-to-video-api.json
```

Send the output back here. We will then wire the exact patch paths for prompt, negative prompt, width, height, fps, frame count, and seed.

## Notes

- Colab sessions are temporary. Generated files and downloaded models may disappear when the runtime resets.
- Do not expose the ComfyUI URL publicly for production use.
- Keep the URL temporary and close the runtime when done.
