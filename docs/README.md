# CamTrax Blender add-on — developer docs

Technical documentation for contributors working on this repository (`CamTrax/CamTrax_Blender_Addon`).

This package is a Blender Python add-on that imports CamTrax `.Trx` recordings into a Blender scene. Recording/capture happens in the separate CamTrax iOS app; this repo only implements Blender-side import and related UI.

## Contents

| Document | Topics |
|----------|--------|
| [Architecture](architecture.md) | Module layout, registration, UI, operators, data flow |
| [`.Trx` format](trx-format.md) | JSON schema and companion media as consumed by the importer |
| [Development](development.md) | Local setup, packaging, versioning, constraints |
| [Implementation notes](implementation-notes.md) | Coordinate conversion, compositor graph, shadow catcher, known code quirks |

## Quick map of the repository

```
.
├── __init__.py              # Entire add-on (bl_info, panel, operators, register/unregister)
├── blender_manifest.toml    # Blender extension manifest (id, version, min Blender)
├── assets/
│   └── logo2.png            # Panel header icon
├── LICENSE                  # MIT text file in repo root
├── README.md                # End-user documentation
├── AGENTS.md                # Instructions for AI coding agents
└── docs/                    # Developer documentation (this folder)
```

There is no separate package layout, test suite, CI config, database, authentication, or environment-variable configuration in this repository.

## Upstream / product context

- Product site: [https://camtrax.io](https://camtrax.io)
- Blender Python API: [https://docs.blender.org/api/current/](https://docs.blender.org/api/current/)
- Blender extensions / manifests: [https://docs.blender.org/manual/en/latest/advanced/extensions/](https://docs.blender.org/manual/en/latest/advanced/extensions/)

Document Blender APIs only in terms of how this add-on uses them; prefer linking upstream manuals for generic behavior.
