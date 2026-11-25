# Sources and credits

PatchGuard does not claim ownership of third-party work.

## Project foundations

- [Morphe patches template](https://github.com/MorpheApp/morphe-patches-template) — official template used for the PatchGuard bundle, build configuration and release pipeline. GPL-3.0; see `LICENSE` and `NOTICE`.
- [Morphe Patcher](https://github.com/MorpheApp/morphe-patcher) and [Morphe documentation](https://github.com/MorpheApp/morphe-documentation) — patch API and development guidance.
- [Morphe Manager](https://github.com/MorpheApp/morphe-manager) — documented patch-source behavior.

Morphe is referenced only as a compatible platform. No Morphe logo or official endorsement is claimed.

## Cataloged sources

Initial intake on 2026-11-25 recorded three community sources:

- [xob0t/morphe-patches](https://github.com/xob0t/morphe-patches) — GPL-3.0, HEAD `b88dbe8c8bc8517005a7308865fd92023b6a2358`.
- [Basil-AS/ru-apps-patches](https://github.com/Basil-AS/ru-apps-patches) — GPL-3.0, HEAD `942c2ac926673db3c49c1a581ed3a9891e47023c`.
- [Jl4cTuk/morphe-patches](https://github.com/Jl4cTuk/morphe-patches) — GPL-3.0, HEAD `8670317938ee76d0968fde57379ff57b52a79f69`.

Basil-AS source comments explicitly credit xob0t and Jl4cTuk for ported code. Those notices must be preserved if code is later reused.

Every future source and patch record must contain:

- Original author.
- Original repository.
- Exact source commit.
- License.
- Reused files, if any.
- Modifications made by PatchGuard.
- Related issues, pull requests and documentation.
- Attribution text.

PatchGuard links to sources it does not have the right to redistribute. It does not copy third-party code without a compatible license. No external patch has been approved, merged or distributed.

## Tools

Static analysis tools, their versions and licenses are recorded in `tools/tools_manifest.yml` when the toolchain is installed. PatchGuard does not relicense third-party tools.

## Corrections

If you believe your work is used without proper attribution, open an issue or contact the maintainer through GitHub. Corrections are made in the repository history.
