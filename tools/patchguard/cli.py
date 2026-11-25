"""PatchGuard command-line interface.

Stage 0 implements the local, static-only foundation: database initialization,
status, schema validation, export and backup. Collection, audit and update
commands are added in later stages and must not bypass the static-only policy.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from . import __version__
from .config import ConfigError, find_project_root, load_config, path_for
from .db import connect, counts, distribution_counts, init_database, require_initialized, status_counts
from .logging import setup_logging
from .validation import format_issues, validate_catalog

EXIT_OK = 0
EXIT_ERROR = 1
EXIT_USAGE = 2
EXIT_VALIDATION = 3
EXIT_POLICY = 4
EXIT_DB = 5
EXIT_ENV = 6


def _root(args: argparse.Namespace) -> Path:
    return (args.root or find_project_root()).resolve()


def _config(args: argparse.Namespace) -> dict[str, Any]:
    return load_config(_root(args))


def _db_path(config: dict[str, Any]) -> Path:
    path = path_for(config, "database")
    if path is None:
        raise ConfigError("paths.database is not configured")
    return path


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_init(args: argparse.Namespace) -> int:
    root = _root(args)
    config = _config(args)
    db_path = _db_path(config)
    result = init_database(root, db_path)

    if args.seed:
        sys.path.insert(0, str(root))
        from database.seed import seed_from_catalog  # type: ignore[import-not-found]

        connection = connect(db_path)
        try:
            seeded = seed_from_catalog(root, connection)
        finally:
            connection.close()
        result["seeded"] = seeded

    if args.json:
        _print_json(result)
    else:
        print(f"Database: {result['database']}")
        print(f"Schema version: {result['schema_version']}")
        if result["new_migrations"]:
            print(f"Applied migrations: {result['new_migrations']}")
        else:
            print("Applied migrations: none (already up to date)")
        if "seeded" in result:
            print(f"Seeded: {result['seeded']}")
    return EXIT_OK


def cmd_status(args: argparse.Namespace) -> int:
    config = _config(args)
    db_path = _db_path(config)
    if not db_path.is_file():
        message = f"Database not initialized: {db_path}. Run 'patchguard init'."
        if args.json:
            _print_json({"initialized": False, "database": str(db_path), "error": message})
        else:
            print(message, file=sys.stderr)
        return EXIT_DB

    connection = connect(db_path)
    try:
        require_initialized(connection)
        payload = {
            "database": str(db_path),
            "audit_model": (config.get("audit") or {}).get("mode"),
            "runtime_testing": (config.get("audit") or {}).get("runtime_testing"),
            "apk_testing": (config.get("audit") or {}).get("apk_testing"),
            "compatibility_runtime_verification": (config.get("audit") or {}).get(
                "compatibility_runtime_verification"
            ),
            "counts": counts(connection),
            "audit_status": status_counts(connection),
            "distribution_status": distribution_counts(connection),
        }
    finally:
        connection.close()

    if args.json:
        _print_json(payload)
    else:
        print(f"Database: {payload['database']}")
        print(f"Audit model: {payload['audit_model']}")
        print(f"Runtime testing: {payload['runtime_testing']}")
        print(f"APK testing: {payload['apk_testing']}")
        print("Counts:")
        for table, count in payload["counts"].items():
            print(f"  {table}: {count}")
        if payload["audit_status"]:
            print("Patch audit status:")
            for status, count in payload["audit_status"].items():
                print(f"  {status}: {count}")
        if payload["distribution_status"]:
            print("Patch distribution status:")
            for status, count in payload["distribution_status"].items():
                print(f"  {status}: {count}")
    return EXIT_OK


def cmd_validate(args: argparse.Namespace) -> int:
    root = _root(args)
    issues = validate_catalog(root)
    if args.json:
        _print_json([{"path": issue.path, "message": issue.message} for issue in issues])
    else:
        print(format_issues(issues))
    return EXIT_VALIDATION if issues else EXIT_OK


def _query_all(connection: sqlite3.Connection, table: str) -> list[dict[str, Any]]:
    try:
        rows = connection.execute(f"SELECT * FROM {table}").fetchall()
    except sqlite3.OperationalError:
        return []
    return [dict(row) for row in rows]


def cmd_export(args: argparse.Namespace) -> int:
    config = _config(args)
    db_path = _db_path(config)
    if not db_path.is_file():
        print(f"Database not initialized: {db_path}", file=sys.stderr)
        return EXIT_DB

    connection = connect(db_path)
    try:
        require_initialized(connection)
        payload = {
            "exported_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
            "project": (config.get("project") or {}).get("name"),
            "audit_model": (config.get("audit") or {}).get("mode"),
            "runtime_tested": False,
            "apk_tested": False,
            "compatibility_runtime_verified": False,
            "applications": _query_all(connection, "applications"),
            "sources": _query_all(connection, "sources"),
            "source_revisions": _query_all(connection, "source_revisions"),
            "patches": _query_all(connection, "patches"),
            "audits": _query_all(connection, "audits"),
            "findings": _query_all(connection, "findings"),
            "dependencies": _query_all(connection, "dependencies"),
            "compatibility_assessments": _query_all(connection, "compatibility_assessments"),
            "attribution": _query_all(connection, "attribution"),
            "update_checks": _query_all(connection, "update_checks"),
            "releases": _query_all(connection, "releases"),
            "decisions": _query_all(connection, "decisions"),
        }
    finally:
        connection.close()

    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    if args.output == "-":
        print(text)
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
        print(f"Exported to {output}")
    return EXIT_OK


def cmd_backup(args: argparse.Namespace) -> int:
    root = _root(args)
    config = _config(args)
    db_path = _db_path(config)
    output_dir = Path(args.output) if args.output else root / ".patchguard" / "backups"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = output_dir / f"patchguard-backup-{stamp}.zip"

    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        if db_path.is_file():
            zf.write(db_path, ".patchguard/patchguard.sqlite3")
        for relative in (
            "config",
            "catalog",
            "audits",
            "reports",
            "schemas",
            "database",
            "docs",
        ):
            directory = root / relative
            if not directory.exists():
                continue
            for path in sorted(directory.rglob("*")):
                if path.is_file():
                    zf.write(path, path.relative_to(root).as_posix())
        for name in ("README.md", "SECURITY.md", "SECURITY_POLICY.md", "THREAT_MODEL.md", "NOTICE", "LICENSE"):
            path = root / name
            if path.is_file():
                zf.write(path, name)

    if args.json:
        _print_json({"archive": str(archive), "bytes": archive.stat().st_size})
    else:
        print(f"Backup written: {archive} ({archive.stat().st_size} bytes)")
    return EXIT_OK


def cmd_doctor(args: argparse.Namespace) -> int:
    checks: list[dict[str, Any]] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "ok": ok, "detail": detail})

    add("python", sys.version_info >= (3, 12), sys.version.split()[0])
    try:
        import yaml  # noqa: F401

        add("pyyaml", True, "importable")
    except Exception as exc:  # pragma: no cover - environment-specific
        add("pyyaml", False, str(exc))
    try:
        import jsonschema  # noqa: F401

        add("jsonschema", True, "importable")
    except Exception as exc:  # pragma: no cover - environment-specific
        add("jsonschema", False, str(exc))
    add("git", shutil.which("git") is not None, shutil.which("git") or "not found")

    try:
        config = _config(args)
        audit = config.get("audit") or {}
        static_only = (
            audit.get("mode") == "static-only"
            and audit.get("runtime_testing") is False
            and audit.get("apk_testing") is False
            and audit.get("compatibility_runtime_verification") is False
        )
        add("static-only configuration", static_only, f"mode={audit.get('mode')}")
        db_path = _db_path(config)
        add("database present", db_path.is_file(), str(db_path))
    except ConfigError as exc:
        add("configuration", False, str(exc))

    ok = all(check["ok"] for check in checks)
    if args.json:
        _print_json({"ok": ok, "checks": checks})
    else:
        for check in checks:
            marker = "OK" if check["ok"] else "FAIL"
            print(f"[{marker}] {check['check']}: {check['detail']}")
        print("Doctor result:", "OK" if ok else "FAILED")
    return EXIT_OK if ok else EXIT_ENV


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="patchguard",
        description="Static-only review tooling for PatchGuard Android Patches.",
    )
    parser.add_argument("--root", type=Path, help="Repository root (default: auto-detect)")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON where supported")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create the local database and apply migrations")
    init_parser.add_argument("--seed", action="store_true", help="Import catalog YAML into the database")
    init_parser.set_defaults(func=cmd_init)

    status_parser = subparsers.add_parser("status", help="Show database and catalog status")
    status_parser.set_defaults(func=cmd_status)

    validate_parser = subparsers.add_parser("validate", help="Validate catalog, audit and policy records")
    validate_parser.set_defaults(func=cmd_validate)

    export_parser = subparsers.add_parser("export", help="Export the working database as JSON")
    export_parser.add_argument("--output", default="-", help="Output path, or '-' for stdout")
    export_parser.set_defaults(func=cmd_export)

    backup_parser = subparsers.add_parser("backup", help="Create a local backup archive")
    backup_parser.add_argument("--output", help="Backup directory")
    backup_parser.set_defaults(func=cmd_backup)

    doctor_parser = subparsers.add_parser("doctor", help="Check the local environment and configuration")
    doctor_parser.set_defaults(func=cmd_doctor)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logger = setup_logging(verbose=getattr(args, "verbose", False))
    try:
        return int(args.func(args))
    except ConfigError as exc:
        logger.error("Configuration error: %s", exc)
        return EXIT_ENV
    except RuntimeError as exc:
        logger.error("Runtime error: %s", exc)
        return EXIT_ERROR
    except KeyboardInterrupt:
        logger.error("Interrupted")
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
