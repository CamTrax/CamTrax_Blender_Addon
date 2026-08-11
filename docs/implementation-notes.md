# Implementation notes

Details that matter when modifying [`__init__.py`](../__init__.py). Prefer this over re-deriving behavior from the long nested `execute()` body.

## File and path conventions

- Import UI filter is case-sensitive to the glob `*.Trx` (capital `T`).
- Sibling media paths use `filepath.replace('-camera.Trx', '-video.mp4')` (and similarly for segmentation / render output). Renaming the suffix convention requires coordinated changes in every `replace` call site inside `execute`.

## Nested functions inside the import operator

`SNA_OT_Import_48Be2.execute` defines helpers **inside** the method:

1. A first `create_node_graph` (plate → rotate → scale → composite/viewer only)
2. `import_Trxfile`
3. A **second** `create_node_graph` (full plate + Render Layers mix + segmentation mask chain)

In Python, the second definition **replaces** the first. Only the full compositor graph runs. The earlier function body is currently dead code. If you refactor, delete the unused definition or extract one shared helper to the module level.

## Compositor graph (active)

Approximate node flow after import:

```text
MovieClip(video) → Rotate → Scale(SCENE_SIZE) ──→ MixRGB image slot 1 ──→ Composite
                                              ↘→ MixRGB Fac ← SegmentationMix
RenderLayers Image ──────────────────────────→ MixRGB image slot 2
RenderLayers Alpha ──→ Multiply ←── Blur2 ← DilateErode ← Blur1 ← Invert ← Exposure ← Scale(RELATIVE) ← Scale(RENDER_SIZE) ← MovieClip(segmentation)
```

Labeled frames in the tree:

- `ADJUST THESE FOR THE SEGMENTATION MASK SIZE AND FEATHER` — relative scale, exposure, invert, blur, dilate/erode
- `TURN SEGMENTATION ON AND OFF` — mix node with default `Fac = 0` (segmentation off until the user raises Fac)

Default exposure on the mask path is `3`. Blur sizes are hardcoded (20 then 10, Mitch filter).

## Camera background vs compositor orientation

Portrait and landscape-right adjust both the camera background image and the compositor rotate node. Landscape-left and upside-down have limited or no dedicated background/compositor rotation branches.

## Shadow catcher operator coupling

`sna.shadow_992d5` hard-codes:

- Object name: `Horizontal Plane [1]`
- Scene name: `Scene` (via `bpy.data.scenes['Scene']`)

It does not search the import root or the current selection. Imports that lack a first plane with alignment that capitalizes to `Horizontal`, or that run in a non-default scene name, will error at poll/execute.

Poll returns false when that plane already `is_shadow_catcher`, which disables the button after a successful enable.

## Preview icons

`load_preview_icon` caches paths in the global `_icons` preview collection. Missing files return icon id `0`. The panel always resolves `assets/logo2.png` relative to `__file__`.

## Unused / no-op surfaces

- `ExportHelper` is imported but unused.
- `addon_keymaps` is never populated.
- Panel `poll` is `return not (False)` (always true).
- Import `poll` is effectively always true; `sna_path` is set from the panel to `os.path.basename(r'')` (empty) before the file browser supplies `filepath`.

## Orientation branch quirk

Camera rotation selection includes:

```python
elif video_orientation == ROTATE_LANDSCAPE_RIGHT:
```

`ROTATE_LANDSCAPE_RIGHT` is a **matrix**, while `video_orientation` is an **int**. The intended check is almost certainly `ORIENTATION_LANDSCAPE_RIGHT` (`4`). As written, that branch does not run for normal integer orientation values; landscape-right still gets compositor/background handling via other `== ORIENTATION_LANDSCAPE_RIGHT` checks. Fix carefully and test with a landscape-right recording if changing this.

## Safe modification guidelines

1. Preserve `.Trx` key names and the `-camera.Trx` / `-video.mp4` / `-segmentation.mp4` suffix contract unless updating producer + docs together.
2. Keep `UNITY2BLENDER` conversion on all imported transforms unless intentionally changing the coordinate basis.
3. Avoid renaming `bl_idname`s (`sna.import_48be2`, `sna.shadow_992d5`, panel id) without a migration note.
4. Do not add network calls or secrets; the add-on is offline file import only.
5. When splitting `__init__.py` into modules, retain a top-level `register` / `unregister` and valid `bl_info` / manifest for Blender discovery.
