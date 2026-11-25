"""Database seeding from public catalog YAML.

The database is a local index; catalog YAML remains the public source of truth.
Running this seed is safe to repeat: rows are upserted by stable slug.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from patchguard.db import utc_now  # noqa: E402


def _load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _json(value: Any) -> str:
    return json.dumps(value if value is not None else [], ensure_ascii=False)


def seed_from_catalog(root: Path, connection) -> dict[str, int]:
    """Upsert applications, sources, patches, attribution and compatibility."""
    now = utc_now()
    counts = {"applications": 0, "sources": 0, "patches": 0, "attribution": 0, "compatibility": 0}

    for path in sorted((root / "catalog" / "apps").glob("*.yml")):
        app = _load(path)
        if not isinstance(app, dict):
            continue
        connection.execute(
            """
            INSERT INTO applications
                (slug, name, package_name, developer, category, security_class,
                 supported_versions, official_website, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name = excluded.name,
                package_name = excluded.package_name,
                developer = excluded.developer,
                category = excluded.category,
                security_class = excluded.security_class,
                supported_versions = excluded.supported_versions,
                official_website = excluded.official_website,
                notes = excluded.notes,
                updated_at = excluded.updated_at
            """,
            (
                app["slug"],
                app["name"],
                app["package_name"],
                app.get("developer"),
                app["category"],
                app.get("security_class", "NORMAL"),
                _json(app.get("supported_versions", [])),
                app.get("official_website"),
                app.get("notes"),
                now,
                now,
            ),
        )
        counts["applications"] += 1

    for path in sorted((root / "catalog" / "sources").glob("*.yml")):
        source = _load(path)
        if not isinstance(source, dict):
            continue
        connection.execute(
            """
            INSERT INTO sources
                (slug, name, repository_url, host, owner, source_type, license,
                 license_evidence, trust_level, tracked_branch, last_checked_commit,
                 latest_release, last_checked_at, repository_status, aliases, notes,
                 created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name = excluded.name,
                repository_url = excluded.repository_url,
                host = excluded.host,
                owner = excluded.owner,
                source_type = excluded.source_type,
                license = excluded.license,
                license_evidence = excluded.license_evidence,
                trust_level = excluded.trust_level,
                tracked_branch = excluded.tracked_branch,
                last_checked_commit = excluded.last_checked_commit,
                latest_release = excluded.latest_release,
                last_checked_at = excluded.last_checked_at,
                repository_status = excluded.repository_status,
                aliases = excluded.aliases,
                notes = excluded.notes,
                updated_at = excluded.updated_at
            """,
            (
                source["slug"],
                source["name"],
                source["repository_url"],
                source["host"],
                source["owner"],
                source["source_type"],
                source["license"],
                source.get("license_evidence"),
                source["trust_level"],
                source["tracked_branch"],
                source.get("last_checked_commit"),
                source.get("latest_release"),
                source.get("last_checked_at"),
                source.get("repository_status", "UNKNOWN"),
                _json(source.get("aliases", [])),
                source.get("notes"),
                now,
                now,
            ),
        )
        counts["sources"] += 1

    app_ids = {
        row["slug"]: row["id"]
        for row in connection.execute("SELECT id, slug FROM applications").fetchall()
    }
    source_ids = {
        row["slug"]: row["id"]
        for row in connection.execute("SELECT id, slug FROM sources").fetchall()
    }

    for path in sorted((root / "catalog" / "patches").rglob("*.yml")):
        patch = _load(path)
        if not isinstance(patch, dict):
            continue
        app_slug = patch.get("application")
        source_slug = patch.get("source")
        if app_slug not in app_ids:
            raise ValueError(f"{path}: unknown application {app_slug!r}")
        if source_slug not in source_ids:
            raise ValueError(f"{path}: unknown source {source_slug!r}")

        connection.execute(
            """
            INSERT INTO patches
                (slug, name, application_id, source_id, source_commit, source_sha256,
                 original_author, description, functionality, category, version,
                 supported_app_versions, required_patcher_version, dependencies,
                 modified_components, permissions, network_activity, audit_status,
                 distribution_status, audit_scope, runtime_tested, apk_tested,
                 compatibility_runtime_verified, risk_score, confidence_level,
                 audit_tools, audit_limitations, last_audited_at, last_updated_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(slug) DO UPDATE SET
                name = excluded.name,
                application_id = excluded.application_id,
                source_id = excluded.source_id,
                source_commit = excluded.source_commit,
                source_sha256 = excluded.source_sha256,
                original_author = excluded.original_author,
                description = excluded.description,
                functionality = excluded.functionality,
                category = excluded.category,
                version = excluded.version,
                supported_app_versions = excluded.supported_app_versions,
                required_patcher_version = excluded.required_patcher_version,
                dependencies = excluded.dependencies,
                modified_components = excluded.modified_components,
                permissions = excluded.permissions,
                network_activity = excluded.network_activity,
                audit_status = excluded.audit_status,
                distribution_status = excluded.distribution_status,
                audit_scope = excluded.audit_scope,
                risk_score = excluded.risk_score,
                confidence_level = excluded.confidence_level,
                audit_tools = excluded.audit_tools,
                audit_limitations = excluded.audit_limitations,
                last_audited_at = excluded.last_audited_at,
                last_updated_at = excluded.last_updated_at,
                notes = excluded.notes
            """,
            (
                patch["slug"],
                patch["name"],
                app_ids[app_slug],
                source_ids[source_slug],
                patch["source_commit"],
                patch["source_sha256"],
                patch.get("original_author"),
                patch.get("description"),
                patch.get("functionality"),
                patch["category"],
                patch.get("version"),
                _json(patch.get("supported_app_versions", [])),
                patch.get("required_patcher_version"),
                _json(patch.get("dependencies", [])),
                _json(patch.get("modified_components", [])),
                _json(patch.get("permissions", [])),
                _json(patch.get("network_activity", [])),
                patch["audit_status"],
                patch["distribution_status"],
                patch.get("audit_scope", "SOURCE_CODE_ONLY"),
                patch.get("risk_score"),
                patch.get("confidence_level"),
                _json(patch.get("audit_tools", [])),
                _json(patch.get("audit_limitations", [])),
                patch.get("last_audited_at"),
                patch.get("last_updated_at"),
                patch.get("notes"),
            ),
        )
        counts["patches"] += 1

        patch_id = connection.execute("SELECT id FROM patches WHERE slug = ?", (patch["slug"],)).fetchone()["id"]
        attribution = patch.get("attribution")
        if isinstance(attribution, dict):
            connection.execute(
                """
                INSERT INTO attribution
                    (patch_id, original_author, original_repository, source_commit,
                     source_license, inspiration_source, related_issue, related_pull_request,
                     upstream_documentation, reused_files, modifications, attribution_text)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(patch_id) DO UPDATE SET
                    original_author = excluded.original_author,
                    original_repository = excluded.original_repository,
                    source_commit = excluded.source_commit,
                    source_license = excluded.source_license,
                    inspiration_source = excluded.inspiration_source,
                    related_issue = excluded.related_issue,
                    related_pull_request = excluded.related_pull_request,
                    upstream_documentation = excluded.upstream_documentation,
                    reused_files = excluded.reused_files,
                    modifications = excluded.modifications,
                    attribution_text = excluded.attribution_text
                """,
                (
                    patch_id,
                    attribution.get("original_author"),
                    attribution.get("original_repository"),
                    attribution.get("source_commit"),
                    attribution.get("source_license"),
                    attribution.get("inspiration_source"),
                    attribution.get("related_issue"),
                    attribution.get("related_pull_request"),
                    attribution.get("upstream_documentation"),
                    _json(attribution.get("reused_files", [])),
                    attribution.get("modifications"),
                    attribution.get("attribution_text"),
                ),
            )
            counts["attribution"] += 1

        compatibility = patch.get("compatibility")
        if isinstance(compatibility, list):
            connection.execute(
                "DELETE FROM compatibility_assessments WHERE patch_id = ?", (patch_id,)
            )
            for item in compatibility:
                if not isinstance(item, dict):
                    continue
                connection.execute(
                    """
                    INSERT INTO compatibility_assessments
                        (patch_id, app_version, version_code, basis, evidence, notes, assessed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        patch_id,
                        item.get("app_version"),
                        item.get("version_code"),
                        item.get("basis", "NOT_RUNTIME_TESTED"),
                        item.get("evidence"),
                        item.get("notes"),
                        patch.get("last_audited_at"),
                    ),
                )
                counts["compatibility"] += 1

    connection.commit()
    return counts


def main() -> int:
    import argparse

    from patchguard.config import load_config, path_for
    from patchguard.db import connect

    parser = argparse.ArgumentParser(description="Seed the PatchGuard database from catalog YAML.")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    config = load_config(root)
    db_path = path_for(config, "database")
    if db_path is None:
        raise SystemExit("paths.database is not configured")
    connection = connect(db_path)
    try:
        result = seed_from_catalog(root, connection)
    finally:
        connection.close()
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
