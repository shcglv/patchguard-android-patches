from __future__ import annotations

from pathlib import Path

from patchguard.config import find_project_root, load_config, path_for


ROOT = Path(__file__).resolve().parents[2]


def test_find_project_root() -> None:
    assert find_project_root(ROOT) == ROOT


def test_static_only_configuration() -> None:
    config = load_config(ROOT)
    audit = config["audit"]
    assert audit["mode"] == "static-only"
    assert audit["runtime_testing"] is False
    assert audit["apk_testing"] is False
    assert audit["compatibility_runtime_verification"] is False
    assert audit["max_confidence"] == "MEDIUM"


def test_database_path_is_local() -> None:
    config = load_config(ROOT)
    database = path_for(config, "database")
    assert database is not None
    assert database.name == "patchguard.sqlite3"
    assert ".patchguard" in database.parts
