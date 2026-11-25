# Sources

This document lists external sources tracked by PatchGuard, their provenance, license and review status. The machine-readable source of truth is `catalog/sources/`.

## Source policy

PatchGuard only tracks public sources that can be pinned to an exact commit. Every source record includes:

- Repository URL and host.
- Owner and source type.
- License and license evidence.
- Trust level and repository status.
- Tracked branch, last checked commit and last checked time.
- Latest known release.
- Review status and links to audit records.

No source is considered trusted merely because it is popular or hosted by a known organization. Each reviewed revision is evaluated on its own evidence.

## Tracked sources

Initial intake completed on 2026-11-25. See [the intake report](docs/catalog/initial-intake-2026-11-25.md). These are outstanding community sources, not approved or fully audited.

| Source | Owner | License | Trust | Latest release | Last checked commit | Status |
|---|---|---|---|---|---|---|
| [xob0t/morphe-patches](https://github.com/xob0t/morphe-patches) | xob0t | GPL-3.0 | COMMUNITY | v1.14.19 | `b88dbe8c8bc8517005a7308865fd92023b6a2358` | ACTIVE |
| [Basil-AS/ru-apps-patches](https://github.com/Basil-AS/ru-apps-patches) | Basil-AS | GPL-3.0 | COMMUNITY | v1.4.0 | `942c2ac926673db3c49c1a581ed3a9891e47023c` | ACTIVE |
| [Jl4cTuk/morphe-patches](https://github.com/Jl4cTuk/morphe-patches) | Jl4cTuk | GPL-3.0 | COMMUNITY | v1.4.0 | `8670317938ee76d0968fde57379ff57b52a79f69` | ACTIVE |

All three sources are pinned to a specific commit. Presence in this table does not imply trust, approval, or runtime compatibility.

## Source status meanings

| Status | Meaning |
|---|---|
| `ACTIVE` | Repository is reachable and tracked. |
| `ARCHIVED` | Upstream repository is archived. |
| `RENAMED` | Repository was renamed; URL and aliases were updated. |
| `UNAVAILABLE` | Repository or release is unreachable. |
| `UNKNOWN` | Status could not be determined. |

## Attribution

For each source and patch, PatchGuard records the original author, repository, commit, license, reused files (if any) and modifications. If PatchGuard only links to a source and does not reuse code, this is stated explicitly.

If you are a source author and believe an attribution is incomplete or incorrect, please open an issue or contact the maintainer through GitHub.
