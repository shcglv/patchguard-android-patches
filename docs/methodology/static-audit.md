# Static-only audit methodology

PatchGuard reviews **patch code**, not the runtime behavior of a target application. This page explains exactly what is reviewed, what is not, and how to interpret a `STATICALLY REVIEWED` status.

## 1. Why static-only

Android patch bundles modify application bytecode. Testing a patch end-to-end requires an original APK, a decompiler, an emulator or device, a test account, and often an account with real data. That process is difficult to isolate, hard to reproduce, and creates legal and privacy risks.

PatchGuard instead answers a narrower and more reproducible question:

> Is the patch source safe to distribute as far as source-level evidence can establish, and what remains unknown?

This is not a claim that the patch works, is compatible, or is safe at runtime.

## 2. What PatchGuard analyzes

### 2.1. Source code

- Kotlin, Java, Smali (when present in the source repository), XML, Gradle/Kotlin DSL, JavaScript, Shell, JSON, YAML, properties, ProGuard rules and resources.
- Patch declarations, compatibility metadata, fingerprints, hooks, injection points and extension code.
- Dead code, unused classes, suspiciously broad hooks, reflection, dynamic class loading, file access, clipboard access, token handling and crypto APIs.
- Build scripts, Gradle plugins, repository declarations and CI workflows that affect the produced bundle.
- Network APIs and string literals: URLs, domains, IP addresses, HTTP clients, request bodies and identifiers passed to them.

### 2.2. Provenance

- Repository owner, default branch, exact commit SHA, tags and releases.
- Commit history, related pull requests and issues, renames and forks.
- Author identity where available, and consistency between the claimed and actual origin.
- License file, SPDX identifier, copyright notices and redistribution terms.
- SHA-256 of the reviewed source tree and files.

### 2.3. Dependencies

- Gradle/Maven coordinates, versions and repositories.
- npm packages and lockfiles, when present.
- Licenses and known vulnerabilities (CVE/OSV).
- Whether dependency versions changed since the previous review.
- SBOM generation where the source format allows it.

### 2.4. Secrets

- API keys, tokens, private keys, passwords, credentials, unexpected certificates.
- Secrets in source and, where feasible, in commit history.
- Findings are reported by location and type only; values are never published.

## 3. What PatchGuard does not do

- It does not download target APKs.
- It does not decompile target applications or extract DEX/native libraries.
- It does not install applications or modified APKs.
- It does not run Android Emulator or AVD.
- It does not create test accounts.
- It does not run the patch against a real application.
- It does not perform dynamic network monitoring.
- It does not verify that a fingerprint matches a real app version.
- It does not prove that a patch is free of runtime-only malicious behavior.

## 4. Checks performed

| Area | What is checked | Typical evidence |
|---|---|---|
| Provenance | Repository, author, commit, history, license | Commit SHA, API metadata, license file |
| Source review | Logic, hooks, reflection, dynamic loading, file/network access | File/line references, code excerpts |
| Dependencies | Coordinates, versions, licenses, CVEs, changes | SBOM, OSV results, diff |
| Network (static) | URLs, domains, IPs, HTTP APIs, data passed | String/API evidence |
| Manifest/permissions | Permissions/components declared in source or extension | Manifest snippets |
| Secrets | Keys, tokens, credentials, certificates | Redacted location only |
| Build/CI | Gradle plugins, repositories, workflow steps | Build script evidence |
| Integrity | SHA-256 of source tree and artifacts | Hash manifest |
| Compatibility | Declared metadata, fingerprints, version gates | Static assessment only |

## 5. Tools

PatchGuard may use:

- **Semgrep** with project-specific rules for Android/Kotlin/Java patch patterns.
- **Gitleaks** for secret detection.
- **Trivy** and **OSV-Scanner** for dependency and vulnerability data.
- **Syft** for SBOM generation where useful.
- Custom Python checks for patch metadata, fingerprints, build scripts and source inventory.
- Git and GitHub/GitLab APIs for provenance.

Tools are pinned by version and, where distributed as binaries, by SHA-256. Source code is not uploaded to public third-party scanning services without explicit owner permission.

## 6. What cannot be established statically

- Runtime behavior and side effects.
- Actual network connections, including destinations constructed at runtime.
- Whether a fingerprint matches a specific app version.
- Whether a patch applies cleanly or causes crashes.
- Whether a patch actually removes ads, changes UI, or preserves functionality.
- Whether a server-side component behaves maliciously.
- Whether obfuscated or native code contains hidden behavior.
- Whether the absence of findings means the absence of vulnerabilities.

## 7. Why no findings does not mean safe

Static analysis is evidence, not proof. A reviewer can miss a subtle data flow, an obfuscated branch, a native payload, a server-side trigger, or a behavior that only appears under specific conditions. A clean report means:

> No issues were found in the reviewed scope, with the stated coverage and limitations.

It does not mean:

> The patch is safe.

PatchGuard therefore caps confidence at `MEDIUM` and never uses `HIGH` in the static-only model. The absence of findings does not raise confidence to the maximum.

## 8. Why compatibility is not confirmed without running the app

Compatibility claims depend on:

- The exact target app version and version code.
- The app's obfuscation map and class/method shapes.
- Fingerprint precision and fallback behavior.
- Patcher and Manager versions.
- Device/API-level behavior.

Reading a patch's declared `Compatibility` block and fingerprints is useful, but it cannot prove that the fingerprint matches the target build. Without running the patcher against the app, compatibility is at most `STATICALLY_ASSESSED`. It is always labeled `NOT_RUNTIME_TESTED`.

## 9. Status and confidence

- `STATICALLY_REVIEWED` — the planned static checks for a specific source revision are complete.
- `UNVERIFIED` — not enough data for a meaningful review.
- `REJECTED` — failed review or policy.
- `BLOCKED` — a critical finding or policy prohibition.
- `UPDATE_AVAILABLE` — upstream changed; re-review required.

Confidence:

- `LOW` — partial source, missing dependencies, unclear license or limited coverage.
- `MEDIUM` — full source, provenance, license, dependencies and static checks completed; runtime still unknown.
- `HIGH` — not used. Runtime behavior is not observed.

## 10. Audit Scope block

Every patch card must contain an honest scope block:

```markdown
### Audit Scope

- Source code: Reviewed
- Dependencies: Reviewed / Not reviewed
- Runtime: Not Tested
- Target APK: Not Tested
- Compatibility: Static Assessment Only
- Dynamic network: Not Tested
```

Fields reflect the actual review. `Reviewed` is not filled in automatically.

## 11. Reading a report

1. Check the exact source commit and SHA-256.
2. Read the coverage and limitations before the findings.
3. Treat `STATICALLY_REVIEWED` as “static checks completed”, not “safe”.
4. Check whether compatibility is `DECLARED`, `STATICALLY_ASSESSED`, or `NOT_RUNTIME_TESTED`.
5. For critical applications, expect `BLOCKED` and read-only analysis only.
6. If the patch is distributed, verify the release signature and recorded hash.

## 12. Reporting a problem with an audit

If you believe an audit missed a security-relevant issue, use GitHub private vulnerability reporting as described in [Security policy](../security-policy.md). Do not open a public issue with exploit details.
