# Security policy

The full policy is in [SECURITY_POLICY.md](https://github.com/shcglv/patchguard-android-patches/blob/dev/SECURITY_POLICY.md). This page summarizes the parts that affect users and contributors.

## Static-only model

PatchGuard reviews source code and metadata. It does not download target APKs, decompile applications, run emulators, install modified apps, or verify runtime behavior.

## What is in scope

- PatchGuard tooling and CI.
- PatchGuard's own patch and extension code.
- Catalog records and audit evidence.
- Release integrity and signatures.

## What is out of scope

- Vulnerabilities in target applications.
- Runtime behavior of third-party patches.
- Issues that require a modified APK, rooted device, emulator, or real account.

## Reporting

Use GitHub private vulnerability reporting:

https://github.com/shcglv/patchguard-android-patches/security/advisories/new

Do not open a public issue with exploit details.

## Critical applications

Banking, payment, crypto wallet, password manager, authenticator and financial management apps are `CRITICAL`. They are analyzed read-only and are never included in a distributed bundle by default.

## Claims

PatchGuard does not describe patches as “safe”, “fully tested”, or “runtime verified”. The correct terms are “statically reviewed”, “no findings in the reviewed scope”, and “not runtime tested”.
