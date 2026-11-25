from __future__ import annotations

import sqlite3
from pathlib import Path

import pytest

from patchguard.db import apply_migrations, connect, counts, init_database

ROOT = Path(__file__).resolve().parents[2]


def test_init_database_is_idempotent(tmp_path: Path) -> None:
    db_path = tmp_path / "patchguard.sqlite3"
    first = init_database(ROOT, db_path)
    second = init_database(ROOT, db_path)
    assert first["new_migrations"] == [1]
    assert second["new_migrations"] == []
    assert db_path.is_file()

    connection = connect(db_path)
    try:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert "patches" in tables
        assert "audits" in tables
        assert "decisions" in tables
        assert counts(connection)["patches"] == 0
    finally:
        connection.close()


def test_append_only_audit_history(tmp_path: Path) -> None:
    db_path = tmp_path / "patchguard.sqlite3"
    init_database(ROOT, db_path)
    connection = connect(db_path)
    try:
        now = "2026-11-25T00:00:00Z"
        connection.execute(
            "INSERT INTO applications (slug, name, package_name, category, created_at, updated_at) "
            "VALUES ('app', 'App', 'com.example.app', 'tools', ?, ?)",
            (now, now),
        )
        connection.execute(
            "INSERT INTO sources (slug, name, repository_url, host, owner, source_type, license, "
            "trust_level, tracked_branch, created_at, updated_at) "
            "VALUES ('src', 'Source', 'https://github.com/example/src', 'github.com', 'example', "
            "'github_repository', 'GPL-3.0-only', 'COMMUNITY', 'main', ?, ?)",
            (now, now),
        )
        connection.execute(
            "INSERT INTO patches (slug, name, application_id, source_id, source_commit, source_sha256, "
            "category, audit_status, distribution_status, audit_scope, runtime_tested, apk_tested, "
            "compatibility_runtime_verified) "
            "VALUES ('app/patch', 'Patch', 1, 1, ?, ?, 'ADVERTISING', 'STATICALLY_REVIEWED', "
            "'NOT_ELIGIBLE', 'SOURCE_CODE_ONLY', 0, 0, 0)",
            ("0" * 40, "0" * 64),
        )
        connection.execute(
            "INSERT INTO audits (audit_id, patch_id, source_commit, source_sha256, audit_date, "
            "audit_type, auditor, report_path, audit_result) "
            "VALUES ('audit-1', 1, ?, ?, ?, 'INITIAL', 'tester', 'audits/records/x/audit.yml', "
            "'STATICALLY_REVIEWED')",
            ("0" * 40, "0" * 64, now),
        )
        connection.commit()

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("UPDATE audits SET auditor = 'other' WHERE audit_id = 'audit-1'")
        connection.rollback()

        with pytest.raises(sqlite3.IntegrityError):
            connection.execute("DELETE FROM audits WHERE audit_id = 'audit-1'")
        connection.rollback()
    finally:
        connection.close()


def test_migration_checksum_tamper_detection(tmp_path: Path) -> None:
    migration = tmp_path / "0001_test.sql"
    migration.write_text("CREATE TABLE test (id INTEGER PRIMARY KEY);", encoding="utf-8")
    db_path = tmp_path / "db.sqlite3"
    connection = connect(db_path)
    try:
        assert apply_migrations(connection, tmp_path) == [1]
        assert apply_migrations(connection, tmp_path) == []

        migration.write_text(
            "CREATE TABLE test (id INTEGER PRIMARY KEY);\n-- changed after apply\n",
            encoding="utf-8",
        )
        with pytest.raises(RuntimeError, match="checksum mismatch"):
            apply_migrations(connection, tmp_path)
    finally:
        connection.close()
