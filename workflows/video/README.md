# Video Workflows

Store ComfyUI workflow JSON files here.

Expected first workflow:

- Wan 2.2 text-to-video
- Wan 2.2 image-to-video

Do not commit large model weights to this repository.

Suggested names:

- `wan-text-to-video-ui.json` for the ComfyUI UI workflow template
- `wan-text-to-video-api.json` for the backend-submittable API prompt format
- `wan-image-to-video.json`

The backend currently expects a single API-format workflow path from `WAN_WORKFLOW_PATH`.

After exporting a real API workflow, inspect the node IDs and provide request-time `metadata.workflow_patches` for values that should change per generation, such as prompt, negative prompt, width, height, fps, and duration.
