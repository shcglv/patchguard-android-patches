"""SQLite helpers for the local PatchGuard working database.

The database is a local, rebuildable index. Public data lives in Git under
catalog/ and audits/.
"""

from __future__ import annotations

import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def connect(db_path: Path) -> sqlite3.Connection:
    """Open a SQLite connection with the required pragmas."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(db_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA journal_mode = WAL")
    connection.execute("PRAGMA synchronous = NORMAL")
    return connection


def _applied_migrations(connection: sqlite3.Connection) -> dict[int, str]:
    table = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'schema_migrations'"
    ).fetchone()
    if table is None:
        return {}
    return {
        int(row["version"]): str(row["checksum"])
        for row in connection.execute("SELECT version, checksum FROM schema_migrations")
    }


def apply_migrations(connection: sqlite3.Connection, migrations_dir: Path) -> list[int]:
    """Apply pending SQL migrations in filename order. Returns applied versions."""
    if not migrations_dir.is_dir():
        raise FileNotFoundError(f"Migrations directory not found: {migrations_dir}")

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version     INTEGER PRIMARY KEY,
            applied_at  TEXT NOT NULL,
            checksum    TEXT NOT NULL
        )
        """
    )
    connection.commit()

    applied = _applied_migrations(connection)
    newly_applied: list[int] = []

    for migration in sorted(migrations_dir.glob("*.sql")):
        try:
            version = int(migration.stem.split("_", 1)[0])
        except (ValueError, IndexError) as exc:
            raise ValueError(f"Invalid migration filename: {migration.name}") from exc

        sql = migration.read_text(encoding="utf-8")
        checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()

        if version in applied:
            if applied[version] != checksum:
                raise RuntimeError(
                    f"Migration checksum mismatch for {migration.name}: "
                    "the file changed after it was applied. Create a new migration instead."
                )
            continue

        connection.executescript(sql)
        connection.execute(
            "INSERT INTO schema_migrations (version, applied_at, checksum) VALUES (?, ?, ?)",
            (version, utc_now(), checksum),
        )
        connection.commit()
        newly_applied.append(version)

    if not newly_applied and not applied:
        raise RuntimeError("No migrations were applied and no schema version was recorded.")

    return newly_applied


def init_database(root: Path, db_path: Path) -> dict[str, object]:
    """Create the database and apply migrations. Idempotent."""
    connection = connect(db_path)
    try:
        applied = apply_migrations(connection, root / "database" / "migrations")
        return {
            "database": str(db_path),
            "new_migrations": applied,
            "schema_version": SCHEMA_VERSION,
        }
    finally:
        connection.close()


def counts(connection: sqlite3.Connection) -> dict[str, int]:
    """Return row counts for the main catalog tables."""
    result: dict[str, int] = {}
    for table in (
        "applications",
        "sources",
        "source_revisions",
        "patches",
        "audits",
        "findings",
        "dependencies",
        "attribution",
        "update_checks",
        "releases",
        "decisions",
    ):
        try:
            result[table] = int(connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
        except sqlite3.OperationalError:
            result[table] = 0
    return result


def status_counts(connection: sqlite3.Connection) -> dict[str, int]:
    """Return patch counts grouped by audit status."""
    rows = connection.execute(
        "SELECT audit_status, COUNT(*) AS count FROM patches GROUP BY audit_status ORDER BY audit_status"
    ).fetchall()
    return {str(row["audit_status"]): int(row["count"]) for row in rows}


def distribution_counts(connection: sqlite3.Connection) -> dict[str, int]:
    rows = connection.execute(
        "SELECT distribution_status, COUNT(*) AS count FROM patches GROUP BY distribution_status"
    ).fetchall()
    return {str(row["distribution_status"]): int(row["count"]) for row in rows}


def require_initialized(connection: sqlite3.Connection) -> None:
    row = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'patches'"
    ).fetchone()
    if row is None:
        raise RuntimeError("Database is not initialized. Run 'patchguard init' first.")
