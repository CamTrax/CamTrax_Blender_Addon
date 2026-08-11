# `.Trx` format (as consumed by this add-on)

This document describes the **JSON structure and companion files that the Blender importer reads**. It is derived from [`__init__.py`](../__init__.py) (`import_Trxfile` / `create_node_graph`). The CamTrax iOS app is the producer of these assets; this repo does not define an exporter.

> **Naming:** The importer derives sibling paths by string-replacing `'-camera.Trx'` on the selected file path. Recordings should use that suffix convention.

## Companion media

| Path pattern | Usage in add-on |
|--------------|-----------------|
| `{base}-camera.Trx` | Tracking JSON (`json.load`) |
| `{base}-video.mp4` | Camera background movie clip; compositor `CompositorNodeMovieClip`; sequencer sound strip `background_audio` |
| `{base}-segmentation.mp4` | Compositor segmentation movie clip |
| `{base}-blender-render.mp4` | Default `scene.render.filepath` after import (output target, not an input) |

If companion videos are missing, Blender’s movie-clip / sound loading will fail at import time.

## Top-level JSON object

```json
{
  "render_data": { },
  "camera_frames": { },
  "planes": [ ],
  "tracked_transforms": [ ]
}
```

Missing keys are tolerated where the code uses `.get(...)` with defaults; **`render_data` fields used for resolution and orientation are accessed with direct indexing** and must be present.

### `render_data`

| Key | Type | Required | Behavior |
|-----|------|----------|----------|
| `video_resolution_x` | number | yes | `scene.render.resolution_x` |
| `video_resolution_y` | number | yes | `scene.render.resolution_y` |
| `orientation` | int | yes | Device orientation; drives camera background and compositor rotate (see below) |
| `fps` | number | no | Defaults to `60` if omitted; sets `scene.render.fps` and frame mapping |

#### Orientation values (importer constants)

| Value | Constant | Notes in importer |
|-------|----------|-------------------|
| `1` | `ORIENTATION_PORTRAIT` | Background crop + 90° rotation; compositor rotate −90°; camera rotation matrix portrait |
| `2` | `ORIENTATION_UPSIDE_DOWN` | Defined; no dedicated branch beyond default identity camera rotation |
| `3` | `ORIENTATION_LANDSCAPE_LEFT` | Camera rotation uses landscape-left matrix (currently 0° Z) |
| `4` | `ORIENTATION_LANDSCAPE_RIGHT` | Background rotation 180°; compositor rotate 180° |

### `camera_frames`

Expected shape:

```json
{
  "timestamps": [0.0, 0.016, "..."],
  "transforms": [ [ [/* 4x4 */] ], "..."],
  "datas": [ [focal_length_mm, sensor_height], "..." ]
}
```

| Field | Usage |
|-------|--------|
| `timestamps` | Seconds; last value × FPS sets `scene.frame_end` (ceil, min 1). Each timestamp maps to frame `max(ceil(ts * fps), 1)`. |
| `transforms` | 4×4 matrices; applied as `UNITY2BLENDER @ (mat @ camera_rotation)` to `cam.matrix_world`, then LocRot keyframed |
| `datas` | Per-frame `[focal_length, sensor_height]` written to `cam.data.lens` / `cam.data.sensor_height` with lens keyframes |

Index mismatches between the three arrays are skipped via `IndexError` handling (that frame is omitted).

### `planes`

Array of objects:

```json
{
  "alignment": "horizontal",
  "transform": [ [/* 4x4 */] ]
}
```

| Field | Usage |
|-------|--------|
| `alignment` | Capitalized into object name: `"{Alignment} Plane [{n}]"` (1-based index) |
| `transform` | World matrix after `UNITY2BLENDER @ Matrix(transform)` |

Created objects are unit planes (`primitive_plane_add` size 1), parented to `Imported Tracking Data`, wire display, `hide_render = True`, and various visibility flags cleared (including legacy `cycles_visibility` when present).

**Shadow catcher dependency:** The **Enable Shadow Catcher** operator looks up the hard-coded name `Horizontal Plane [1]`. That name appears when the first plane’s `alignment` is `horizontal` (case depends on capitalize of the JSON string).

### `tracked_transforms`

Array of 4×4 matrices. Each becomes an empty named `Empty [{n}]` (1-based), display size `0.2`, parented to the import root, with `matrix_world = UNITY2BLENDER @ Matrix(tfm)`.

## Coordinate conversion

Importer constant `UNITY2BLENDER`:

```text
((-1,  0,  0, 0),
 ( 0,  0, -1, 0),
 ( 0,  1,  0, 0),
 ( 0,  0,  0, 1))
```

Camera and plane/empty transforms from the file are converted with this matrix so ARKit/Unity-style coordinates land in Blender’s coordinate system.

## Scene side effects on import

When `create_nodes=True` (always, from the panel operator):

- `scene.use_nodes = True`; existing compositor nodes are removed and rebuilt
- `scene.view_settings.view_transform = 'Standard'`
- `scene.render.filepath` → `*-blender-render.mp4`
- `scene.render.image_settings.file_format = 'FFMPEG'`
- `scene.render.ffmpeg.format = 'MPEG4'`, `constant_rate_factor = 'HIGH'`

Always:

- `scene.render.film_transparent = True`
- `scene.render.ffmpeg.audio_codec = 'AAC'`
- Sequence editor created if missing; sound strip added from the video file
