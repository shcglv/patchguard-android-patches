# Audit records

Audit records are immutable evidence. They are never deleted or rewritten.

## Layout

```text
audits/records/<patch-slug>/<audit-id>/
├── report.md       # human-readable report
├── audit.yml       # machine-readable summary, validated by schemas/audit.schema.json
├── findings.yml    # optional detailed findings
├── coverage.yml    # what was reviewed and what was not
├── hashes.json     # source tree/file hashes
└── tools.json      # tool names, versions and hashes
```

`audits/by-status/` contains generated index pages for convenience. It is not the canonical record.

## Rules

- Every record is tied to an exact `source_commit` and `source_sha256`.
- `audit_scope` is `SOURCE_CODE_ONLY`.
- `runtime_tested`, `apk_tested` and `compatibility_runtime_verified` are always `false`.
- `limitations` must explain what could not be established.
- Findings must include severity, location, evidence and remediation where possible.
- Secret values are never included; only redacted locations and descriptions.
- A new source revision gets a new audit record. Status is not inherited.
- `STATICALLY_REVIEWED` requires documented limitations.

## Status directories

The per-status index is generated from the records. If you need to find every reviewed patch, search `audit.yml` for `result: STATICALLY_REVIEWED`; do not infer status from a directory name.
