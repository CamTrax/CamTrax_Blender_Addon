# Development

## Prerequisites

- Blender **3.0+** installed locally for manual testing ([Blender download](https://www.blender.org/download/))
- Familiarity with the [Blender Python API](https://docs.blender.org/api/current/)
- No additional pip packages are declared or required by this add-on

## Load the add-on for development

**Option A — Install from zip (matches end-user install)**

1. Zip the repository so `__init__.py` is at the zip root (alongside `assets/` and `blender_manifest.toml`).
2. **Edit → Preferences → Add-ons → Install…**
3. Enable **CamTrax**.

**Option B — Develop from a clone**

1. Symlink or copy this repository into Blender’s add-ons directory, **or** use **Install from Disk** pointing at the folder that contains `__init__.py`.
2. Enable the add-on and use **Reload Scripts** after edits (or restart Blender). Preview icons may require a full disable/enable cycle because `bpy.utils.previews` is created in `register()`.

No virtualenv, `requirements.txt`, or Makefile is required.

## Versioning

Keep these in sync when bumping a release:

| Location | Fields |
|----------|--------|
| `blender_manifest.toml` | `version` |
| `__init__.py` `bl_info` | `"version": (major, minor, patch)` |
| Panel UI string | hardcoded `CamTrax v1.0.0` label in `SNA_PT_CAMTRAX_PANEL_4FD3F.draw` |

Current declared version: **1.0.0**. Minimum Blender: **3.0.0**.

## Packaging / release

1. Ensure `assets/logo2.png` is included.
2. Produce a zip whose root contains `__init__.py`, `blender_manifest.toml`, `assets/`, and any docs you choose to ship.
3. Distribute the zip for **Preferences → Add-ons → Install…**, or as a Blender 4.2+ extension using the manifest (`id = "camtrax"`).

## Testing

There is **no automated test suite**. Manually verify:

1. Import a complete recording set (`*-camera.Trx`, `*-video.mp4`, `*-segmentation.mp4`).
2. Confirm camera animation, background plate, audio strip, planes, empties, and compositor nodes.
3. Confirm **Enable Shadow Catcher** with a first horizontal plane present.
4. Smoke-test portrait and landscape-right recordings (those orientations have dedicated branches).

## Linting / formatting

No project linter or formatter config is present. Prefer changes that stay consistent with the existing single-file style when editing `__init__.py`.

## License files

| Artifact | Declaration |
|----------|-------------|
| `LICENSE` | MIT License text |
| `blender_manifest.toml` | `SPDX:GPL-2.0-or-later` |
| `__init__.py` header | GPLv3-or-later style notice |

Resolve any redistribution license questions with the maintainers before publishing builds.

## Related repositories

- **Blender add-on:** `CamTrax/CamTrax_Blender_Addon`
- **iOS app / exporter:** [`studiobloom/CamTrax`](https://github.com/studiobloom/CamTrax)

Use the iOS repo to confirm exported filenames and `.Trx` shape. Keep this repo’s docs aligned with what the importer actually reads.
