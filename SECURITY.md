# Security Policy

PatchGuard Android Patches is an independent, static-only review project for Android patch code used with Morphe-compatible patch bundles.

## Supported versions

Security fixes are applied to the current `main` branch and, where practical, to the latest stable release of the PatchGuard bundle. Older releases may remain available for reproducibility but are not actively supported.

| Version | Supported |
|---|---|
| Latest stable release | Yes |
| Latest pre-release on `dev` | Best effort |
| Older releases | No |

## What is in scope

- PatchGuard's own Python tooling, schemas, CI workflows and release scripts.
- PatchGuard's own Morphe-compatible patch code and extension code.
- The integrity of PatchGuard's catalog records, audit reports and generated documentation.
- The integrity of PatchGuard release artifacts, signatures and published hashes.
- A cataloged third-party patch where the issue is in PatchGuard's analysis, attribution, or published evidence.

## What is out of scope

- Vulnerabilities in the target Android applications themselves.
- Runtime behavior of third-party patches. PatchGuard does not run target apps or patched builds.
- Vulnerabilities that require a modified APK, a rooted device, an emulator, or a real user account to demonstrate.
- Security of third-party repositories, release infrastructure, or maintainers.
- Disagreements about a patch's usefulness, features, or compatibility that are not security issues.

## How to report

Use GitHub private vulnerability reporting:

**https://github.com/shcglv/patchguard-android-patches/security/advisories/new**

Do not open a public issue for a suspected vulnerability. If private reporting is unavailable, open a minimal public issue asking for a private contact channel and do not include exploit details.

Please include:

- A clear description of the issue and its impact.
- Affected file, commit, release, or catalog record.
- Reproduction steps that do not require an APK or a live target app.
- Any evidence, logs, or proof-of-concept code that is safe to share.
- Whether you want public credit, and under what name.

Do not include real secrets, tokens, personal data, or third-party proprietary code in a report. If a secret is involved, describe its location and type only; do not paste the value.

## What to expect

- Acknowledgement: best effort, usually within 7 days.
- Triage: we will confirm scope, severity and whether a fix or documentation change is needed.
- Fix: timeline depends on severity and complexity. There is no bug bounty.
- Disclosure: coordinated disclosure through the GitHub advisory after a fix or mitigation is available. We will credit reporters who ask to be credited.

## Safe harbor

We will not pursue legal action against researchers who act in good faith, stay within this scope, avoid privacy violations and service disruption, and give us reasonable time to respond before public disclosure. This statement does not bind third parties.

## Static-only limitation

PatchGuard cannot verify runtime behavior, actual network traffic, or compatibility with a target application. A report that depends on running a target app is outside this project's model. We will still document credible static evidence of malicious or unsafe patch behavior.

## Release integrity

PatchGuard release artifacts are published through the official Morphe template release workflow. Releases may be signed; the public key is published in `patches-bundle.json`. If you believe a release was modified after publication, verify the signature and the recorded SHA-256, then report the discrepancy privately.
