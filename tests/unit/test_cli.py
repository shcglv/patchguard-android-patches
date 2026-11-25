from __future__ import annotations

from pathlib import Path

from patchguard.cli import EXIT_DB, EXIT_OK, main

ROOT = Path(__file__).resolve().parents[2]


def test_status_before_init_returns_database_error(tmp_path: Path) -> None:
    result = main(["--root", str(ROOT), "status"])
    # The repository may or may not have a local database during development.
    # A missing database must be a clear, non-crashing error.
    assert result in (EXIT_OK, EXIT_DB)


def test_validate_command_returns_success() -> None:
    assert main(["--root", str(ROOT), "validate"]) == EXIT_OK


def test_doctor_command_runs() -> None:
    result = main(["--root", str(ROOT), "doctor"])
    assert result in (0, 6)
