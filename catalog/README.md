# Catalog

The catalog is the public, machine-readable record of applications, sources, patches, decisions and releases.

## Layout

```text
catalog/
├── apps/<package>.yml
├── sources/<host>-<owner>-<repo>.yml
├── patches/<package>/<patch-slug>.yml
├── decisions/<date>-<patch-slug>.yml
├── releases/<version>.yml
├── community.yml
└── wishlist.yml
```

## Rules

- YAML is the source of truth. SQLite is a local index.
- Every record is validated against `schemas/`.
- Every patch references an existing application and source.
- Every patch records `source_commit`, `source_sha256`, `audit_scope`, `runtime_tested`, `apk_tested`, `compatibility_runtime_verified`, `audit_limitations`.
- Critical applications must have `distribution_status: BLOCKED`.
- `APPROVED` requires a matching decision record with `approved_by`.
- No placeholder or invented records. An empty catalog is valid.

## Example patch record

```yaml
slug: com.example.app/example-patch
name: Example patch
application: com.example.app
source: github-example-patches
source_commit: "0123456789abcdef0123456789abcdef01234567"
source_sha256: "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
category: ADVERTISING
audit_status: STATICALLY_REVIEWED
distribution_status: NOT_ELIGIBLE
audit_scope: SOURCE_CODE_ONLY
runtime_tested: false
apk_tested: false
compatibility_runtime_verified: false
audit_limitations:
  - Runtime behavior was not observed.
  - No target APK was downloaded or tested.
last_audited_at: "2026-11-25T00:00:00Z"
```

The example is illustrative only; it is not a catalog entry.
