# AGENTS.md — CamTrax Blender Add-on

Repository-wide instructions for AI coding agents working on **CamTrax/CamTrax_Blender_Addon**.

## What this project is

A **Blender Python add-on** that imports CamTrax `.Trx` AR tracking files into Blender (camera animation, planes, empties, plate/segmentation compositor setup, sequencer audio).

| Fact | Detail |
|------|--------|
| Primary code | `__init__.py` (single module) |
| Manifest | `blender_manifest.toml` (`id = "camtrax"`, min Blender `3.0.0`) |
| UI | 3D Viewport sidebar category **CamTrax** |
| Operators | `sna.import_48be2`, `sna.shadow_992d5` |
| Assets | `assets/logo2.png` |

User docs: [`README.md`](README.md). Developer docs: [`docs/`](docs/).

## Architecture context

- Dependencies: Blender’s `bpy` / `mathutils` / `bpy_extras.io_utils.ImportHelper` + stdlib `json`, `os`, `math`.
- `.Trx` is JSON; companion `*-video.mp4` and `*-segmentation.mp4` are required for a full import. Schema as consumed: [`docs/trx-format.md`](docs/trx-format.md).
- Transforms are converted with the `UNITY2BLENDER` matrix before assignment to Blender objects.

## Conventions

- Operator/panel class names use existing `SNA_*` identifiers and `bl_idname`s; do not rename casually.
- Prefer minimal diffs. This file is intentionally dense; avoid drive-by refactors of the large nested `execute()` unless the task requires it.
- When changing user-facing behavior, update `README.md` and the relevant `docs/*.md` in the same change.
- Keep `bl_info["version"]`, `blender_manifest.toml` `version`, and the panel version label synchronized.
- Do **not** document or implement features that are not present in this repo.

## Build / test / lint

| Action | Command / method |
|--------|------------------|
| Install | Zip add-on root → Blender **Preferences → Add-ons → Install…** |
| Test | Manual import of a real CamTrax recording set inside Blender |
| Lint | No project linter configured |
| Automated tests | None |

There is no `npm`/`pytest`/`make` workflow. Do not invent CI unless asked.

## Important constraints

1. **Suffix contract:** Path logic assumes `'-camera.Trx'` → `'-video.mp4'` / `'-segmentation.mp4'` / `'-blender-render.mp4'`.
2. **Shadow catcher:** Hard-codes object `Horizontal Plane [1]` and scene `Scene`.
3. **License mismatch:** Root `LICENSE` is MIT; manifest declares GPL-2.0-or-later; `__init__.py` has a GPLv3-style header. Do not “fix” the license text without an explicit human decision.
4. **No secrets:** Never commit credentials or embed API keys; the add-on has no secret configuration today.
5. **Dead code:** Two `create_node_graph` definitions exist; only the second is active. See [`docs/implementation-notes.md`](docs/implementation-notes.md).
6. **Orientation bug:** Landscape-right camera rotation branch compares an int to `ROTATE_LANDSCAPE_RIGHT` (a matrix). Fix only with oriented test media.

## Safe modification checklist

- [ ] Read `docs/architecture.md` and `docs/implementation-notes.md` before large edits.
- [ ] Preserve `.Trx` field names unless updating format docs and producer expectations together.
- [ ] Manually smoke-test import + shadow catcher after operator changes.
- [ ] Leave `assets/logo2.png` paths working for the panel icon.
- [ ] Do not add unused dependencies or scaffold frameworks.

## Related product code

The CamTrax **iOS** application (recording/export) lives at [`studiobloom/CamTrax`](https://github.com/studiobloom/CamTrax). Use it to verify export naming and JSON shape. This add-on’s behavior must remain consistent with files it actually imports.

## Scoped AGENTS.md

No subdirectory currently needs a nested `AGENTS.md` (single-module add-on). Add one only if a future subpackage introduces materially different build or safety rules.
