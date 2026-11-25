"""Public record discovery, schema lookup and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

import yaml

from .config import ConfigError, load_config, load_yaml, path_for
from .models import ValidationIssue

SCHEMA_FILES = {
    "app": "app.schema.json",
    "source": "source.schema.json",
    "patch": "patch.schema.json",
    "audit": "audit.schema.json",
    "compatibility": "compatibility.schema.json",
    "decision": "decision.schema.json",
    "release": "release.schema.json",
}


def load_schemas(root: Path) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for name, filename in SCHEMA_FILES.items():
        path = root / "schemas" / filename
        try:
            schemas[name] = json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise ConfigError(f"Schema file not found: {path}") from exc
        except json.JSONDecodeError as exc:
            raise ConfigError(f"Invalid JSON schema {path}: {exc}") from exc
    return schemas


def _validator(schema: dict[str, Any]):
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:  # pragma: no cover - dependency error path
        raise ConfigError(
            "The 'jsonschema' package is required for validation. "
            "Install development dependencies with 'pip install -e .[dev]'."
        ) from exc
    return Draft202012Validator(schema)


def validate_document(
    schema: dict[str, Any],
    document: Any,
    path: Path,
    root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for error in sorted(_validator(schema).iter_errors(document), key=lambda item: list(item.path)):
        location = "/".join(str(part) for part in error.path) or "<root>"
        issues.append(ValidationIssue(str(path.relative_to(root)), f"{location}: {error.message}"))
    return issues


def _load_yaml_file(path: Path) -> Any:
    try:
        return load_yaml(path)
    except ConfigError as exc:
        raise ConfigError(str(exc)) from exc


def _iter_yaml(root: Path, pattern: str) -> Iterable[Path]:
    yield from sorted(root.glob(pattern))


def validate_catalog(root: Path) -> list[ValidationIssue]:
    """Validate catalog records and cross-record references.

    Missing directories are treated as empty catalogs.
    """
    schemas = load_schemas(root)
    issues: list[ValidationIssue] = []
    applications: dict[str, dict[str, Any]] = {}
    sources: dict[str, dict[str, Any]] = {}
    patches: dict[str, dict[str, Any]] = {}
    decisions: dict[str, dict[str, Any]] = {}

    for path in _iter_yaml(root, "catalog/apps/*.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["app"], document, path, root))
        if isinstance(document, dict) and isinstance(document.get("slug"), str):
            applications[document["slug"]] = document

    for path in _iter_yaml(root, "catalog/sources/*.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["source"], document, path, root))
        if isinstance(document, dict) and isinstance(document.get("slug"), str):
            sources[document["slug"]] = document

    for path in _iter_yaml(root, "catalog/patches/**/*.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["patch"], document, path, root))
        if not isinstance(document, dict):
            continue
        slug = document.get("slug")
        if not isinstance(slug, str):
            continue
        patches[slug] = document
        app = document.get("application")
        source = document.get("source")
        if app not in applications:
            issues.append(ValidationIssue(str(path.relative_to(root)), f"unknown application: {app}"))
        if source not in sources:
            issues.append(ValidationIssue(str(path.relative_to(root)), f"unknown source: {source}"))
        if app in applications and applications[app].get("security_class") == "CRITICAL":
            if document.get("distribution_status") != "BLOCKED":
                issues.append(
                    ValidationIssue(
                        str(path.relative_to(root)),
                        "critical application must have distribution_status: BLOCKED",
                    )
                )
        if document.get("distribution_status") == "APPROVED":
            if app in applications and applications[app].get("security_class") == "CRITICAL":
                issues.append(
                    ValidationIssue(
                        str(path.relative_to(root)),
                        "critical application cannot be APPROVED for distribution",
                    )
                )

    for path in _iter_yaml(root, "catalog/decisions/*.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["decision"], document, path, root))
        if isinstance(document, dict) and isinstance(document.get("id"), str):
            decisions[document["id"]] = document

    for path in _iter_yaml(root, "audits/records/**/audit.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["audit"], document, path, root))
        if not isinstance(document, dict):
            continue
        patch = document.get("patch")
        if patch not in patches:
            issues.append(ValidationIssue(str(path.relative_to(root)), f"unknown patch: {patch}"))
        if document.get("result") == "STATICALLY_REVIEWED":
            if not document.get("limitations"):
                issues.append(
                    ValidationIssue(
                        str(path.relative_to(root)),
                        "STATICALLY_REVIEWED requires documented limitations",
                    )
                )

    for path in _iter_yaml(root, "catalog/releases/*.yml"):
        document = _load_yaml_file(path)
        issues.extend(validate_document(schemas["release"], document, path, root))

    # APPROVED patches require a matching decision record.
    for slug, patch in patches.items():
        if patch.get("distribution_status") != "APPROVED":
            continue
        matching = [
            decision
            for decision in decisions.values()
            if decision.get("patch") == slug
            and decision.get("new_status") == "APPROVED"
            and decision.get("approved_by")
        ]
        if not matching:
            issues.append(
                ValidationIssue(
                    f"catalog/patches/{slug}.yml",
                    "APPROVED requires a decision record with approved_by",
                )
            )

    issues.extend(_validate_config(root))
    return issues


def _validate_config(root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        config = load_config(root)
    except ConfigError as exc:
        return [ValidationIssue("config/settings.yml", str(exc))]

    audit = config.get("audit") or {}
    required_false = (
        "runtime_testing",
        "apk_testing",
        "compatibility_runtime_verification",
    )
    for key in required_false:
        if audit.get(key) is not False:
            issues.append(
                ValidationIssue(
                    "config/settings.yml",
                    f"audit.{key} must be false in the static-only model",
                )
            )
    if audit.get("mode") != "static-only":
        issues.append(ValidationIssue("config/settings.yml", "audit.mode must be static-only"))
    if audit.get("max_confidence") != "MEDIUM":
        issues.append(ValidationIssue("config/settings.yml", "audit.max_confidence must be MEDIUM"))

    security_policy = load_yaml(root / "config" / "security_policy.yml")
    if isinstance(security_policy, dict):
        model = security_policy.get("audit_model") or {}
        for key in ("runtime_testing", "apk_testing", "decompilation", "emulator", "target_app_installation"):
            if model.get(key) is not False:
                issues.append(
                    ValidationIssue(
                        "config/security_policy.yml",
                        f"audit_model.{key} must be false",
                    )
                )

    return issues


def format_issues(issues: list[ValidationIssue]) -> str:
    if not issues:
        return "OK: all catalog, audit, decision and release records are valid."
    lines = [f"{len(issues)} validation issue(s):"]
    lines.extend(f"  - {issue.render()}" for issue in issues)
    return "\n".join(lines)
