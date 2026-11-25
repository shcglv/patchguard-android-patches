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

At repository bootstrap, no external source has been reviewed. This table is intentionally empty rather than populated with placeholder data.

| Source | Owner | License | Trust | Last checked commit | Status |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

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
