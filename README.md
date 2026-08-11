<div align="center">
  <img src="assets/logo2.png" alt="CamTrax Logo" width="100">
  <h1><a href="https://camtrax.io">CamTrax</a></h1>
  <p>Blender add-on for importing CamTrax <code>.Trx</code> AR camera tracking recordings</p>
</div>

<div align="center">
  <a href="https://discord.gg/EaVUD78B94">
    <img src="https://img.shields.io/static/v1?label=&message=Join%20our%20Discord%20Community&color=5865F2&style=for-the-badge&logo=discord&logoColor=white" alt="Join our Discord Community">
  </a>
</div>

## What this is

**CamTrax** is a Blender **Import-Export** add-on. It imports `.Trx` tracking files produced by the CamTrax iOS app and rebuilds the recorded camera motion, detected planes, tracked empties, background video, audio, and compositor setup.

Product overview and the iOS recorder: [camtrax.io](https://camtrax.io).

## Requirements

- [Blender](https://www.blender.org/) **3.0** or later (`blender_version_min` / `bl_info` both declare 3.0.0)
- A CamTrax recording set that includes the `.Trx` file and its companion media (see below)

## Install

1. Download or clone this repository.
2. Zip the add-on folder so the zip root contains `__init__.py`, `blender_manifest.toml`, and `assets/` (do not zip only the parent directory that wraps those files incorrectly).
3. In Blender: **Edit → Preferences → Add-ons → Install…** and select the zip.
4. Enable **CamTrax** in the add-on list.

On Blender 4.2+, the included [`blender_manifest.toml`](blender_manifest.toml) also identifies this package as an extension (`id = "camtrax"`, `type = "add-on"`).

## Recording files the importer expects

The import operator filters for `*.Trx`. Paths are derived by replacing the `-camera.Trx` suffix on the chosen file:

| File | Role |
|------|------|
| `*-camera.Trx` | JSON tracking data (camera, planes, empties, render metadata) |
| `*-video.mp4` | Plate video (camera background, compositor movie clip, sequencer audio) |
| `*-segmentation.mp4` | Segmentation mask video used in the compositor graph |

Keep these files together with matching base names. After import, the add-on sets the default render output path to `*-blender-render.mp4` next to the source files.

Current iOS app exports use `.mov` companion videos. Rename or convert them to the `.mp4` names above, or update the importer path replacements before importing.

## How to use

1. Open the **3D Viewport** sidebar (**N**), then the **CamTrax** tab.
2. Click **Import .Trx File** and select a `*-camera.Trx` file.
3. The add-on creates an `Imported Tracking Data` hierarchy with:
   - **ARCamera** — animated camera with lens keyframes and movie-clip background
   - Detected **planes** (wire display; hidden from most render visibility by default)
   - **Empty** objects for tracked transforms
4. Optionally click **Enable Shadow Catcher** after import. This targets the object named `Horizontal Plane [1]`, enables Cycles shadow-catcher mode on it, and switches the scene render engine to **Cycles**.

Import also configures scene FPS/resolution from the `.Trx` data, enables transparent film, builds a compositor node tree (plate + optional segmentation mix), and switches the 3D view to the new camera.

## Developer documentation

Implementation details, architecture, `.Trx` schema as consumed by this add-on, and contribution guidance live under **[docs/](docs/)**.

AI coding agents: see **[AGENTS.md](AGENTS.md)**.

## Links

- Website / docs URL declared in the add-on: [camtrax.io](https://camtrax.io)
- Discord: [discord.gg/EaVUD78B94](https://discord.gg/EaVUD78B94)

## License

This repository includes an [MIT License](LICENSE) file. The Blender extension manifest declares `SPDX:GPL-2.0-or-later`, and `__init__.py` includes a GPLv3-style header. Confirm the intended license before redistributing.
