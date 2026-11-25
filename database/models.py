"""Schema-level constants shared by the database layer and tooling."""

from __future__ import annotations

SCHEMA_VERSION = 1

AUDIT_STATUSES = (
    "DISCOVERED",
    "PENDING",
    "STATIC_AUDITING",
    "STATICALLY_REVIEWED",
    "UNVERIFIED",
    "REJECTED",
    "BLOCKED",
    "UPDATE_AVAILABLE",
    "OUTDATED",
)

DISTRIBUTION_STATUSES = ("NOT_ELIGIBLE", "CANDIDATE", "APPROVED", "BLOCKED")

PATCH_CATEGORIES = (
    "UI",
    "ADVERTISING",
    "PRIVACY",
    "FUNCTIONALITY",
    "NETWORK",
    "SECURITY_SENSITIVE",
)

COMPATIBILITY_BASES = ("DECLARED", "STATICALLY_ASSESSED", "NOT_RUNTIME_TESTED")

SECURITY_CLASSES = ("NORMAL", "CRITICAL")

AUDIT_RESULTS = ("STATICALLY_REVIEWED", "UNVERIFIED", "REJECTED", "BLOCKED")

TABLES = (
    "applications",
    "sources",
    "source_revisions",
    "patches",
    "audits",
    "findings",
    "dependencies",
    "compatibility_assessments",
    "attribution",
    "update_checks",
    "releases",
    "decisions",
    "schema_migrations",
)

STATIC_ONLY_INVARIANTS = {
    "audit_scope": "SOURCE_CODE_ONLY",
    "runtime_tested": False,
    "apk_tested": False,
    "compatibility_runtime_verified": False,
}
