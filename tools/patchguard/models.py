"""Small data models used by the PatchGuard CLI and validators."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Application:
    slug: str
    name: str
    package_name: str
    category: str
    security_class: str = "NORMAL"
    developer: str | None = None
    supported_versions: tuple[str, ...] = ()
    official_website: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class Source:
    slug: str
    name: str
    repository_url: str
    host: str
    owner: str
    source_type: str
    license: str
    trust_level: str
    tracked_branch: str
    repository_status: str = "UNKNOWN"
    last_checked_commit: str | None = None
    latest_release: str | None = None
    last_checked_at: str | None = None
    license_evidence: str | None = None
    aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class Patch:
    slug: str
    name: str
    application: str
    source: str
    source_commit: str
    source_sha256: str
    category: str
    audit_status: str
    distribution_status: str
    audit_scope: str = "SOURCE_CODE_ONLY"
    runtime_tested: bool = False
    apk_tested: bool = False
    compatibility_runtime_verified: bool = False
    last_audited_at: str | None = None
    audit_limitations: tuple[str, ...] = ()
    risk_score: int | None = None
    confidence_level: str | None = None
    audit_ids: tuple[str, ...] = ()
    attribution: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def render(self) -> str:
        return f"{self.path}: {self.message}"
