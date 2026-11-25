# Threat model

The full threat model is in [THREAT_MODEL.md](https://github.com/shcglv/patchguard-android-patches/blob/dev/THREAT_MODEL.md). This page summarizes the assets and the most important residual risks.

## Assets

- PatchGuard signing key.
- Release artifacts and metadata.
- Catalog and audit records.
- Source provenance and attribution.
- CI workflows and secrets.
- Maintainer accounts and user trust.

## Main threats

- Malicious code hidden in a patch.
- Compromised upstream repository or release.
- Dependency and build-plugin compromise.
- Release artifact tampering.
- Signing key theft.
- Account takeover.
- Malicious pull requests or workflow changes.
- Typosquatting and impersonation.
- Misleading status claims.

## Mitigations

- Exact commit pinning and SHA-256 hashes.
- No execution of third-party code.
- Static analysis and human review.
- Critical findings block distribution.
- No automatic `APPROVED`.
- Signed releases and recorded fingerprints.
- Least-privilege CI and pinned actions.
- Branch protection, secret scanning and Dependabot.
- Explicit documentation of limitations.

## Residual risks

- Runtime behavior is not observed.
- Fingerprints and compatibility are not validated against target APKs.
- Static analysis can miss obfuscated, native, or server-side behavior.
- A compromised maintainer account can bypass review controls.
- Users may over-trust a `STATICALLY REVIEWED` label despite warnings.

These risks are accepted as part of the static-only model. They are documented rather than hidden.
