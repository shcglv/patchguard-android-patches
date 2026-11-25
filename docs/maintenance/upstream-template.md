# Upstream template baseline

PatchGuard's own Morphe-compatible bundle is built from the official
[Morphe patches template](https://github.com/MorpheApp/morphe-patches-template).
This page records the exact baseline and every intentional deviation, so a future
template update can be reviewed instead of merged blindly.

## Baseline

| Item | Value |
|---|---|
| Template repository | `MorpheApp/morphe-patches-template` |
| Baseline commit | `4cb966a5aa5ea70725aa5eb4531eea8f0e5549e6` |
| Baseline branches | `main`, `dev` |
| Baseline build | Gradle wrapper 9.9.1, JDK 21, `app.morphe.patches` 2.1.2, `morphe-patcher` 2.5.0 |
| Baseline release | `.github/workflows/release.yml` + `.releaserc` (semantic-release) |
| License | GPL-3.0, with the Morphe NOTICE 7c restriction |

The baseline was imported as a normal Git history (clone of the template), not as a
GitHub fork or a GitHub-template-generated repository. The template commit is in
history; no GitHub “generated from template” badge is required by Morphe Manager or
Community Patches.

## Kept from the template

- `patches/` and `extensions/` Gradle modules and the official build layout.
- `gradle/wrapper`, `gradlew`, `gradlew.bat`, `gradle.properties`.
- `.releaserc` (semantic-release configuration).
- `.github/scripts/generate_patches_readme.py`.
- `package.json` and `package-lock.json` (subject to Dependabot updates).
- Generated-file ownership: `patches-list.json`, `patches-bundle.json`,
  `PATCHES.md` and `CHANGELOG.md` are written by the release workflow, never by hand.
- Branch model: changes on `dev`, stable release by merging `dev` into `main`.
- Semantic commit rules: `feat:`, `fix:`, `chore:`, `docs:`.

## Intentional deviations

| File / area | Change | Reason |
|---|---|---|
| `settings.gradle.kts` | `rootProject.name` is `patchguard-android-patches` | Project identity |
| `patches/build.gradle.kts` | group `app.patchguard`; `about` block updated | Project identity and bundle metadata |
| `patches/src/main/kotlin/app/template/**` | renamed to `app.patchguard.patches.**` | Distinct package, no template naming |
| `extensions/extension/**` | namespace/package renamed to `app.patchguard.extension` | Same |
| `README.md` | replaced with PatchGuard README; generated patch markers retained | Public project page while keeping the official list generator |
| `NOTICE` | Morphe NOTICE preserved; PatchGuard notice appended | GPL/attribution compliance |
| Issue templates | replaced with PatchGuard source suggestion, bug and feature forms | No misleading template links |
| `.github/dependabot.yml` | added `pip` ecosystem on `dev` | Python tooling |
| `.github/workflows/release.yml` | actions pinned by SHA; `push` limited to `main`/`dev`; job gated by `vars.PATCHGUARD_RELEASE_ENABLED == 'true'` | Security pinning and an explicit release gate |
| `.github/workflows/validate.yml` | added | Python tests, schema/catalog validation, strict docs build |
| `catalog/`, `audits/`, `reports/`, `docs/`, `tools/`, `schemas/`, `database/`, `config/`, `tests/` | added | PatchGuard catalog and static-only audit tooling |

`release.yml` was modified in place, not replaced by a new pipeline. When
`PATCHGUARD_RELEASE_ENABLED` is `true`, the official semantic-release flow runs
unchanged: build `.mpp`, generate metadata, sign if configured, publish the GitHub
release, update generated files and backmerge.

## Release gate

`PATCHGUARD_RELEASE_ENABLED` is a repository variable, currently `false`.

To create a release:

1. Complete the static gate for the patch revision.
2. Remove the template Example Patch and any `com.example.app` target.
3. Configure `MORPHE_SIGNING_KEY` and the public key if signing is enabled.
4. Set `PATCHGUARD_RELEASE_ENABLED=true`.
5. Push/merge to `dev` for a pre-release or `main` for a stable release through
   the official workflow.
6. Verify the `.mpp`, `patches-bundle.json`, `patches-list.json`, `PATCHES.md`,
   signature and hashes.
7. Set `PATCHGUARD_RELEASE_ENABLED=false` again after the release, unless a
   deliberate release window remains open.

Do not create releases by hand and do not edit generated files.

## Upstream sync policy

- Do not auto-merge template updates.
- Review changes to `release.yml`, `.releaserc`, the README generator, Gradle
  wrapper and dependency lockfiles.
- Keep the template commit in history and update this page when the baseline
  changes.
- Re-apply SHA pinning after any template action update.
- Re-test a pre-release in a controlled window after a template change.

## Known limitations

- GitHub rejected `sha_pinning_required=true` for this personal repository
  (“all actions must be from a repository owned by shcglv”). Actions are pinned
  manually; the repository setting is `false`.
- Required PR/status-check rules are not enabled yet; the release identity must be
  configured first, otherwise semantic-release cannot push its generated commit.
- No release exists yet; `patches-bundle.json` is still the template placeholder.
  Adding the repository to Morphe Manager before a release will not work.
- This page records technical deviations, not legal advice. Third-party code reuse
  remains subject to GPL-3.0 and the original attribution.
