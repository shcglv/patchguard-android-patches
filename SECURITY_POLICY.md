# Security Policy — PatchGuard Android Patches

This document defines the rules that PatchGuard follows. It is normative for maintainers, contributors and automation.

## 1. Audit model

PatchGuard uses a **static-only** audit model.

- We analyze patch source code, fingerprints, hooks, extensions, build scripts, dependencies, manifests present in source, network strings, secrets, provenance and metadata.
- We do **not** download target APKs, decompile applications, extract DEX or native libraries, install apps, run emulators, create test accounts, or verify runtime behavior.
- We do **not** claim that a patch is safe, working, or runtime-compatible.
- `STATICALLY_REVIEWED` means the planned static checks for a specific source revision were completed. It is not a safety certificate.
- `APPROVED` is a separate owner decision about distribution. It is not an audit result and does not imply runtime verification.

## 2. Source policy

A source is eligible for review only if:

- It is a public GitHub or GitLab repository, or a public release artifact referenced by such a repository.
- The exact revision can be pinned to a commit SHA.
- The license is identifiable, or the source is used only for read-only analysis and linking (no code reuse).
- The source does not require executing untrusted code to inspect it.

Default prohibitions:

- No execution of third-party `gradlew`, `install.sh`, `build.sh`, npm scripts, GitHub Actions, binaries, or tests.
- No submodules, Git LFS payloads, or large binary files during acquisition.
- No APKs, DEX files, native libraries, or decompiled application code.
- No uploading source to public third-party scanning services without explicit owner permission.
- No copying code without a compatible license and attribution.

## 3. Status rules

Audit statuses: `DISCOVERED`, `PENDING`, `STATIC_AUDITING`, `STATICALLY_REVIEWED`, `UNVERIFIED`, `REJECTED`, `BLOCKED`, `UPDATE_AVAILABLE`, `OUTDATED`.

Distribution statuses: `NOT_ELIGIBLE`, `CANDIDATE`, `APPROVED`, `BLOCKED`.

- No patch is `APPROVED` automatically.
- `APPROVED` requires a decision record with `approved_by`, date, reason, evidence and scope.
- A new source revision never inherits the previous revision's status automatically.
- Critical findings override the numeric risk score and force `BLOCKED`.
- `REJECTED` and `BLOCKED` records and their evidence are retained. They are not deleted.

## 4. Critical application policy

The following categories are `CRITICAL`: banking, payments, crypto wallets, password managers, authenticators, and financial management.

For critical applications:

- Only read-only analysis of source and documentation is allowed.
- No patch build, no bundle inclusion, no distribution, no runtime testing.
- No changes to authentication, TLS certificate pinning, integrity checks, anti-fraud, or financial transaction handling.
- The default distribution status is `BLOCKED`. There is no exception for patches named "Remove Ads" or similar.

`config/critical_apps.yml` is the source of truth for known critical packages. An unknown application in a financial category is treated as critical until the owner decides otherwise.

## 5. Risk and confidence

- Risk is scored 0–100 using the dimensions in `config/risk_rules.yml`.
- The score is a heuristic, not a probability of compromise.
- Confidence is `LOW` or `MEDIUM`. `HIGH` is not used in the static-only model because runtime behavior is not observed.
- Missing evidence lowers confidence and may result in `UNVERIFIED`.
- The absence of findings does not increase confidence to the maximum.

## 6. Evidence and integrity

For every review, record:

- Exact source commit SHA.
- SHA-256 of the reviewed source tree and files.
- Tool names and versions.
- Audit date and auditor.
- Scope, coverage and limitations.
- Findings with severity, location, evidence and remediation.
- Attribution and license evidence.

Hashes prove file identity, not safety.

## 7. Build and release policy

- Building PatchGuard's own `.mpp` is allowed only to publish PatchGuard's own bundle.
- The build must not include target APKs and must not install or run applications.
- Third-party patches are never built by PatchGuard.
- Builds run in isolated CI with pinned Gradle and dependencies, minimal permissions, and no signing secrets until the static gate passes.
- Signing keys are never committed, logged, or shared with third-party services.
- Generated files (`patches-list.json`, `patches-bundle.json`, `PATCHES.md`, `CHANGELOG.md`) are not edited by hand.
- Release artifacts are verified for hash and signature before publication is announced.

## 8. CI and supply chain

- GitHub Actions are pinned by full commit SHA.
- Workflows use least-privilege permissions and do not expose secrets to pull requests from forks.
- `pull_request_target` must not execute untrusted code.
- Dependencies are pinned or locked; dependency and secret scanning are enabled.
- Third-party scanner binaries are obtained from official releases and verified by SHA-256.

## 9. Disclosure

- Vulnerability reports are handled through GitHub private security advisories.
- Do not publish exploit details before a fix or mitigation.
- PatchGuard does not operate a bug bounty.

## 10. Incident response

If a signing key, release artifact, or catalog record is suspected to be compromised:

1. Stop publication.
2. Preserve evidence and hashes.
3. Publish a security advisory with affected versions.
4. Rotate keys or revoke artifacts as appropriate.
5. Rebuild and re-sign from a clean checkout.
6. Record the incident and remediation in the repository history.

## 11. Language and claims

Public documentation must not use "safe", "verified working", "fully tested", or equivalent absolute claims. Use precise language: "statically reviewed", "no findings in the reviewed scope", "not runtime tested", "declared compatible".
