# Video Workflows

Store ComfyUI workflow JSON files here.

Expected first workflow:

- Wan 2.2 text-to-video
- Wan 2.2 image-to-video

Do not commit large model weights to this repository.

Suggested names:

- `wan-text-to-video.json`
- `wan-image-to-video.json`

The backend currently expects a single workflow path from `WAN_WORKFLOW_PATH`.

After exporting a real workflow, inspect the node IDs and provide request-time `metadata.workflow_patches` for values that should change per generation, such as prompt, negative prompt, width, height, fps, and duration.
