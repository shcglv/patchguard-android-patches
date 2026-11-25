# Credits

PatchGuard is an independent community project. It is not affiliated with, endorsed by, or maintained by Morphe or the authors of the applications and patches referenced here.

## Project maintainers

- PatchGuard maintainers — project design, tooling, audits, documentation.

## Upstream foundations

- **[Morphe patches template](https://github.com/MorpheApp/morphe-patches-template)** — the official template used for PatchGuard's own Morphe-compatible patch bundle, build configuration and release pipeline. Licensed under GPL-3.0; see `LICENSE` and `NOTICE`.
- **[Morphe Patcher](https://github.com/MorpheApp/morphe-patcher)** and **[Morphe documentation](https://github.com/MorpheApp/morphe-documentation)** — patch API, fingerprinting guidance and development documentation used as reference.
- **[Morphe Manager](https://github.com/MorpheApp/morphe-manager)** — documented patch-source behavior used to validate the structural contract of PatchGuard's bundle.

Morphe is referenced only as a compatible platform. No Morphe logo, branding, or official endorsement is claimed.

## Cataloged sources and patches

Initial intake on 2026-11-25 recorded these community sources:

- **xob0t Morphe Patches** — https://github.com/xob0t/morphe-patches — GPL-3.0.
- **Basil-AS RU Apps Patches** — https://github.com/Basil-AS/ru-apps-patches — GPL-3.0.
- **Jl4cTuk Morphe Patches** — https://github.com/Jl4cTuk/morphe-patches — GPL-3.0.

No third-party patch code has been copied into PatchGuard. The intake records links, provenance and preliminary classifications only. Basil-AS explicitly credits xob0t and Jl4cTuk in its source comments; those notices must be preserved if any code is later reused.

Attribution for each cataloged source and patch is recorded in:

- `catalog/sources/*.yml`
- `catalog/patches/**/*.yml`
- `audits/records/**/report.md`
- `audits/exclusions/**`
- `reports/security/**`
- [`docs/catalog/initial-intake-2026-11-25.md`](docs/catalog/initial-intake-2026-11-25.md)
- `SOURCES.md`

No external patch has been approved, merged or distributed. Entries are not invented.

## Tools

PatchGuard uses open-source tools for static analysis, schema validation and documentation. Tool names, versions and hashes are recorded in `tools/tools_manifest.yml` when the toolchain is implemented. Attribution and licenses are respected.

## Special thanks

- The Morphe community for documenting the patch bundle format and release conventions.
- The maintainers of the static analysis tools used by the project.
- Everyone who reports a security issue responsibly.

If you believe your work is used without proper attribution, please open an issue or contact the maintainer through GitHub so it can be corrected.
