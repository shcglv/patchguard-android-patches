# Threat Model — PatchGuard Android Patches

## 1. Purpose and scope

This threat model covers PatchGuard's repository, tooling, catalog, audit records, own Morphe-compatible patch bundle, release pipeline and public documentation. It does not cover the security of target Android applications, Morphe Manager, or third-party patch authors' infrastructure.

## 2. Assets

| Asset | Why it matters |
|---|---|
| PatchGuard signing key | A compromised key can be used to sign malicious releases that Manager may accept as updates. |
| Release artifacts (`.mpp`) | Users install patched apps built from them. |
| `patches-bundle.json`, `patches-list.json` | Manager reads them to locate and validate releases. |
| Catalog and audit records | Users rely on them to decide whether a patch is trustworthy. |
| Source provenance data | Incorrect provenance can attribute malicious code to an innocent author or hide its origin. |
| CI workflows and secrets | Workflow compromise can publish artifacts or leak secrets. |
| Maintainer accounts | Account takeover can change code, releases, or branch protection. |
| User trust | False claims of safety or testing can cause harm and destroy project credibility. |

## 3. Actors

- Malicious patch author who submits plausible-looking code with hidden behavior.
- Compromised upstream maintainer or repository.
- Typosquatter or impersonator of a legitimate patch project.
- Attacker submitting a pull request or issue with malicious code or workflow changes.
- Attacker who steals a maintainer token, PAT, or signing key.
- Supply-chain attacker in a dependency, Gradle plugin, GitHub Action, or scanner binary.
- Well-intentioned contributor who introduces unsafe code or unverified claims.
- User who misunderstands `STATICALLY_REVIEWED` as a safety guarantee.

## 4. Trust boundaries

```text
Untrusted source repository
        |
        | text-only acquisition, pinned SHA, no execution
        v
Quarantine (local, gitignored)
        |
        | static analysis + human review
        v
Audit records (Git)  --->  Public catalog/docs
        |
        | owner decision
        v
PatchGuard bundle build (isolated CI)
        |
        | static gate, then signing
        v
Signed release artifacts  --->  Morphe Manager
```

- Everything fetched from a third-party source is untrusted input.
- Build scripts and CI configuration from third parties are data, never executable instructions.
- A catalog entry is not an endorsement.
- A signed release proves origin and integrity, not safety.

## 5. Threats and mitigations

| Threat | Impact | Mitigation |
|---|---|---|
| Malicious code hidden in a patch | Users run harmful code | Full source review, Semgrep rules, manual review, critical findings block, no auto-approval |
| Runtime-only malicious behavior | Static review misses it | Explicit limitation; confidence capped at MEDIUM; no safety claims; users warned |
| Compromised upstream release | Malicious code enters catalog | Pin exact SHA, review every revision, update checks, re-audit on change |
| Dependency confusion / malicious package | Build or tooling compromise | Pin versions, lockfiles, verify scanner hashes, review dependency changes |
| Malicious Gradle plugin or GitHub Action | CI compromise | Pin actions by SHA, minimal permissions, no secrets in PR jobs, review build script changes |
| Release artifact tampering | Users install modified bundle | Sign releases, publish public key, verify signature and SHA-256, provenance attestation |
| Signing key theft | Attacker signs malicious release | Key only in secret store, backup offline, 2FA, rotate on suspicion, advisory |
| Account takeover | Unauthorized code/release changes | 2FA, branch protection, PR review, secret scanning, audit logs |
| Malicious pull request | Code execution in CI or repo compromise | No secrets in PR jobs, no `pull_request_target` code execution, static analysis first, maintainer review |
| Typosquatting / impersonation | Users add wrong source | Clear canonical URL, documentation, disclaimer, no lookalike branding |
| False provenance / stolen credit | Legal and trust harm | Record author, repo, commit, license, attribution evidence |
| Misleading status | Users over-trust a patch | Status definitions, `NOT_RUNTIME_TESTED`, docs, review of public claims |
| Data leak via reports | Secrets/PII exposure | Redaction, gitleaks, no raw secrets, private advisories |
| Availability loss | Catalog/history lost | Git history, backups, append-only records, no destructive cleanup |

## 6. Residual risks

- Static analysis cannot observe runtime behavior, server-side logic, obfuscated code, native code, or actual network traffic.
- Fingerprints and compatibility cannot be validated without a target APK; PatchGuard does not claim they are.
- A determined attacker can make malicious behavior indistinguishable in the reviewed source.
- A compromised maintainer account can bypass review controls.
- GitHub, Gradle, Morphe, and scanner supply chains are trusted to some degree; pinning reduces but does not eliminate risk.
- Users may ignore the static-only limitations despite documentation.

## 7. Security invariants

1. No third-party code is executed during analysis.
2. No target APK is downloaded, decompiled, installed, or run.
3. No `APPROVED` status without an explicit owner decision record.
4. No release without a passing static gate and recorded hashes.
5. No secret values in Git, logs, reports, or public documentation.
6. No claim of runtime verification in a static-only project.
7. No deletion of prior audit or decision history.
