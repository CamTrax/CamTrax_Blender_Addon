# CamTrax Blender add-on — developer docs

Technical documentation for contributors working on this repository (`CamTrax/CamTrax_Blender_Addon`).

This package imports CamTrax `.Trx` recordings into Blender. Recording/export context lives in the [CamTrax iOS app repo](https://github.com/studiobloom/CamTrax).

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

## Upstream / product context

- Product site: [https://camtrax.io](https://camtrax.io)
- iOS app / exporter: [https://github.com/studiobloom/CamTrax](https://github.com/studiobloom/CamTrax)
- Blender Python API: [https://docs.blender.org/api/current/](https://docs.blender.org/api/current/)
- Blender extensions / manifests: [https://docs.blender.org/manual/en/latest/advanced/extensions/](https://docs.blender.org/manual/en/latest/advanced/extensions/)

Document Blender APIs only in terms of how this add-on uses them; prefer linking upstream manuals for generic behavior.
