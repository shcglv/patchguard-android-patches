# Contributing to PatchGuard Android Patches

PatchGuard is an independent, static-only review project for Android patch code. Contributions are welcome, but the project has strict rules about provenance, licenses, and what may be submitted.

## Before you contribute

- Read [`SECURITY_POLICY.md`](SECURITY_POLICY.md) and [`THREAT_MODEL.md`](THREAT_MODEL.md).
- Read [`docs/methodology/static-audit.md`](docs/methodology/static-audit.md).
- Do not submit or attach APKs, DEX files, native libraries, decompiled application code, or proprietary material.
- Do not claim that a patch is safe, working, or runtime-compatible. This project does not perform runtime testing.

## Ways to contribute

### 1. Suggest a source or patch for review

Open a **Source / patch suggestion** issue with:

- Public GitHub/GitLab URL.
- Exact revision (commit SHA or release tag).
- App name and package name, if known.
- Patch name and a short description of what it does.
- License and author information, if known.
- Why it is interesting (ads, privacy, UI, functionality, security-sensitive).
- Any known concerns.

Do not paste large code excerpts. A link and exact revision are enough.

### 2. Improve documentation or tooling

Pull requests for docs, schemas, Python tooling, tests, and CI are welcome. Keep changes focused and include tests where behavior changes.

### 3. Contribute patch code

Patch code contributions are accepted only when:

- You are the author, or you have a compatible license and explicit permission to contribute the code.
- The exact origin, author, commit and license are documented.
- The patch follows the official Morphe patch guidelines.
- The code can be reviewed statically; no APK or runtime test is required or accepted as evidence.
- The patch does not target a `CRITICAL` application for distribution.
- The patch does not weaken authentication, TLS pinning, integrity checks, anti-fraud, or financial transaction handling.

Patch code is licensed under GPL-3.0-only unless a compatible third-party license dictates otherwise.

## Branch and commit model

- `dev` is the development and pre-release branch.
- `main` is the stable branch.
- Open pull requests against `dev`.
- Stable releases are produced by merging `dev` into `main` with a merge commit, not a squash.
- Use semantic commit messages:
  - `feat: ...` — new patch or user-facing feature.
  - `fix: ...` — bug fix.
  - `chore: ...` — maintenance that should not create a release.
  - `docs: ...` — documentation only.
- Do not edit generated files: `patches-list.json`, `patches-bundle.json`, `PATCHES.md`, `CHANGELOG.md`.

## Developer Certificate of Origin

By contributing, you certify that you have the right to submit the contribution under the project's license. Sign off your commits:

```text
Signed-off-by: Your Name <your-email@example.com>
```

Use `git commit -s`.

## Pull request checklist

- [ ] The change is focused and explained.
- [ ] No APK, DEX, native library, decompiled app code, or secret is included.
- [ ] No third-party code is included without a compatible license and attribution.
- [ ] No runtime testing is claimed.
- [ ] Documentation is updated, including limitations.
- [ ] Tests pass locally and in CI.
- [ ] Generated files are untouched.
- [ ] The change does not weaken security controls or CI permissions.

## Review process

- All changes go through a pull request and CI.
- The maintainer may request changes, reject a contribution, or close it without merging.
- Security-sensitive changes may require a private discussion.
- Do not pressure for merges or disclose suspected vulnerabilities publicly.

## Licensing

PatchGuard code and documentation are licensed under GPL-3.0-only. By contributing, you agree that your contribution is licensed under the same terms, unless you explicitly mark a compatible third-party file with its original license and attribution.

## Questions

Open a discussion or an issue that does not contain sensitive information. For security reports, use GitHub private vulnerability reporting as described in [`SECURITY.md`](SECURITY.md).
