from __future__ import annotations

from pathlib import Path

from patchguard.validation import load_schemas, validate_catalog, validate_document

ROOT = Path(__file__).resolve().parents[2]


def test_empty_catalog_is_valid() -> None:
    assert validate_catalog(ROOT) == []


def test_patch_schema_rejects_runtime_claims() -> None:
    schemas = load_schemas(ROOT)
    document = {
        "slug": "com.example.app/test",
        "name": "Test",
        "application": "com.example.app",
        "source": "example",
        "source_commit": "0" * 40,
        "source_sha256": "0" * 64,
        "category": "ADVERTISING",
        "audit_status": "STATICALLY_REVIEWED",
        "distribution_status": "NOT_ELIGIBLE",
        "audit_scope": "SOURCE_CODE_ONLY",
        "runtime_tested": True,
        "apk_tested": False,
        "compatibility_runtime_verified": False,
        "last_audited_at": "2026-11-25T00:00:00Z",
        "audit_limitations": ["Runtime behavior was not observed."],
    }
    path = ROOT / "catalog" / "patches" / "example.yml"
    issues = validate_document(schemas["patch"], document, path, ROOT)
    assert issues
    assert any("runtime_tested" in issue.message for issue in issues)


def test_decision_schema_requires_manual_approval() -> None:
    schemas = load_schemas(ROOT)
    document = {
        "id": "decision-1",
        "patch": "com.example.app/test",
        "previous_status": "CANDIDATE",
        "new_status": "APPROVED",
        "decision_reason": "Reviewed and accepted by the owner.",
        "decision_date": "2026-11-25T00:00:00Z",
        "approved_by": "owner",
        "requires_manual_approval": False,
    }
    path = ROOT / "catalog" / "decisions" / "decision-1.yml"
    issues = validate_document(schemas["decision"], document, path, ROOT)
    assert issues
    assert any("requires_manual_approval" in issue.message for issue in issues)
