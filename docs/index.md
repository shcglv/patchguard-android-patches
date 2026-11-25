# PatchGuard documentation

PatchGuard Android Patches is an independent, static-only review project for Android patch code used with Morphe-compatible patch bundles.

> **This is an independent community project. It is not affiliated with, endorsed by, or maintained by Morphe or the authors of the applications and patches referenced here.**

!!! important
    PatchGuard does not download target APKs, decompile applications, run emulators, install modified apps, or verify runtime behavior. A `STATICALLY REVIEWED` status means the static checks for a specific source revision were completed. It is not a safety certificate.

## Start here

- [Static-only audit methodology](methodology/static-audit.md) — what is reviewed and what is not.
- [Statuses](methodology/statuses.md) — what each status means.
- [Risk scoring](methodology/risk-scoring.md) — how the score is calculated.
- [Compatibility](compatibility.md) — why compatibility is not runtime-verified.
- [How to use PatchGuard](how-to-use.md) — adding the source to Morphe Manager, once a release exists.
- [Sources and credits](sources-and-credits.md) — attribution and licensing.
- [Security policy](security-policy.md) — reporting and release integrity.
- [Threat model](threat-model.md) — assets, actors and residual risks.

## Catalog

The catalog is generated from `catalog/` and `audits/`. It contains:

- Applications and their security class.
- Sources with provenance and license.
- Patches with static audit status, risk, confidence, compatibility basis and limitations.
- Audit records with findings and evidence.
- Owner decisions for distribution.

At bootstrap, the catalog is empty. Entries are added only from real reviewed sources; no placeholder patches are invented.

## What “reviewed” means here

PatchGuard's review is intentionally narrow:

1. The exact source revision is pinned and hashed.
2. The patch source, build scripts and dependencies are read.
3. Static tools and project rules look for suspicious patterns.
4. A human reviews the results and documents limitations.
5. The patch receives a static status; runtime behavior remains unknown.

It does not mean the patch works, is compatible with a specific app build, or is safe.
