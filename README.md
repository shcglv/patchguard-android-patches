<div align="center">

<img src="assets/logo.svg" alt="PatchGuard logo" width="96" height="96">

# PatchGuard Android Patches

**Independent, static-only security review of Android patch code for Morphe-compatible bundles.**

[![License: GPL-3.0-only](https://img.shields.io/badge/license-GPL--3.0--only-2ea043.svg)](LICENSE)
[![Audit model: static-only](https://img.shields.io/badge/audit%20model-static--only-f2a93b.svg)](docs/methodology/static-audit.md)
[![Validate](https://github.com/shcglv/patchguard-android-patches/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/shcglv/patchguard-android-patches/actions/workflows/validate.yml)

</div>

> **This is an independent community project. It is not affiliated with, endorsed by, or maintained by Morphe or the authors of the applications and patches referenced here.**

> [!IMPORTANT]
> **Static-only review.** PatchGuard reviews patch source code, dependencies, build scripts, provenance and metadata. It does **not** download target APKs, decompile applications, run Android emulators, install modified apps, or verify runtime behavior. A `STATICALLY REVIEWED` status means the planned static checks for a specific source revision were completed. It does not mean the patch is safe, working, or compatible at runtime.

## What this project is

PatchGuard is a public catalog and audit trail for Android patch code used with Morphe-compatible patch bundles. It focuses on questions that can be answered from source and metadata:

- Where did this patch come from, and which exact revision was reviewed?
- What does the patch code change, and what dependencies does it bring?
- Does it contain suspicious reflection, dynamic code loading, hidden network destinations, secret material, or security-sensitive modifications?
- Is the license compatible with the way the patch is distributed?
- What changed since the last review, and does the new revision require a fresh audit?

The repository also contains PatchGuard's own Morphe-compatible patch bundle. Every PatchGuard patch is reviewed under the same static-only policy before it can be considered for distribution.

## What this project is not

- It is not a malware scanner that can prove an app or patch is safe.
- It is not a runtime compatibility test. No target app is patched or launched here.
- It is not an official Morphe project and does not speak for Morphe.
- It does not distribute third-party APKs or third-party patch code.
- It does not mark a patch as `APPROVED` automatically. `APPROVED` is a separate, explicit owner decision.

## Patch catalog

<!-- PATCHES_START -->
> **[v1.0.0](https://github.com/shcglv/patchguard-android-patches/releases/tag/v1.0.0)**&nbsp;&nbsp;&middot;&nbsp;&nbsp;`main`&nbsp;&nbsp;&middot;&nbsp;&nbsp;**3 patches** across **1 app**&nbsp;&nbsp;&middot;&nbsp;&nbsp;[Full details](PATCHES.md)

| # | App | Patches | Version | Package |
|---|---|---|---|---|
| 1 | [**Ozon**](PATCHES.md#ozon-ruozonappandroid) | 3 | `19.31.0` | [`ru.ozon.app.android`](https://play.google.com/store/apps/details?id=ru.ozon.app.android) |
<!-- PATCHES_END -->

The full audit catalog is in [`catalog/`](catalog/) and the published documentation site. The table above only lists PatchGuard's own bundle; external patches are cataloged separately and are never presented as part of the PatchGuard bundle.

Initial external-source intake (2026-11-25): [docs/catalog/initial-intake-2026-11-25.md](docs/catalog/initial-intake-2026-11-25.md). This is inventory and triage, not approval and not runtime verification.

## Audit status legend

| Status | Meaning |
|---|---|
| `DISCOVERED` | A source or patch was recorded; no review yet. |
| `PENDING` | Queued for static review. |
| `STATIC_AUDITING` | Static review is in progress. |
| `STATICALLY_REVIEWED` | The planned static checks for a specific source revision are complete. Runtime behavior is still unknown. |
| `UNVERIFIED` | Not enough source, metadata, license or provenance data for a meaningful review. |
| `REJECTED` | The patch failed review or policy. |
| `BLOCKED` | A security, license or critical-app policy prevents distribution. |
| `UPDATE_AVAILABLE` | The upstream source changed and a new static review is required. |
| `OUTDATED` | The reviewed revision no longer matches current app or source versions. |

`APPROVED` is not an audit status. It is a separate distribution decision by the project owner and is recorded in `catalog/decisions/`.

## Add to Morphe

<a href="https://morphe.software/add-source?github=shcglv/patchguard-android-patches">
  <img src=".github/assets/add-to-morphe.svg" alt="Add to Morphe" height="48">
</a>

Or add the source manually in **Morphe Manager → Sources → + → Remote**:

```text
https://github.com/shcglv/patchguard-android-patches
```

The `v1.0.0` source publishes three Ozon 19.31.0 UI patches:

- Disable checkout tips
- Hide seller rating prompt
- Show final prices only

The release is **unsigned**; Morphe Manager accepts it while no signing key is
pinned for this source. It is a static-only preview: no target APK was patched or
launched, so compatibility is declared rather than runtime-verified. See the
[v1.0.0 verification report](reports/releases/v1.0.0.md).

> [!WARNING]
> Patch sources decide what ends up inside patched apps. Only add sources you trust. PatchGuard publishes its review evidence, but static review cannot prove runtime safety or compatibility.

## Security methodology

Read [`docs/methodology/static-audit.md`](docs/methodology/static-audit.md) before relying on any status in this repository. In short:

- We review source code, fingerprints, hooks, extensions, build scripts, dependencies, licenses, network strings, secrets and provenance.
- We record exact commit SHAs and SHA-256 hashes.
- We document what we could not verify.
- We never claim that the absence of findings is proof of safety.
- We never claim runtime compatibility without a runtime test, and this project does not perform runtime tests.

## Reporting a vulnerability

Please use GitHub's private vulnerability reporting for this repository:

[Security advisories](https://github.com/shcglv/patchguard-android-patches/security/advisories/new)

Do not open a public issue for a suspected vulnerability in PatchGuard tooling, a PatchGuard patch, or a cataloged third-party patch. See [`SECURITY.md`](SECURITY.md) for scope and expectations.

## Contributing

Contributions are welcome under the terms in [`CONTRIBUTING.md`](CONTRIBUTING.md). In particular:

- Do not submit APKs, DEX files, native libraries, or decompiled application code.
- Do not submit third-party patch code without a compatible license and full attribution.
- Do not claim runtime testing that was not performed.
- All changes go through a pull request and CI.

## Credits and sources

PatchGuard is built on the official [Morphe patches template](https://github.com/MorpheApp/morphe-patches-template) and follows its release conventions. Morphe is mentioned only as a compatible platform. See [`CREDITS.md`](CREDITS.md), [`SOURCES.md`](SOURCES.md), and [`NOTICE`](NOTICE).

## License

PatchGuard code and documentation are licensed under the **GNU General Public License v3.0 only**. See [`LICENSE`](LICENSE). Third-party materials retain their original licenses and are not relicensed by PatchGuard.

---

<div align="center">
<sub>Static review records evidence, not certainty.</sub>
</div>
