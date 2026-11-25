from __future__ import annotations

import shutil
from pathlib import Path

from patchguard.db import connect, init_database
from database.seed import seed_from_catalog

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "sample_catalog"


def test_seed_imports_sample_catalog(tmp_path: Path) -> None:
    db_path = tmp_path / "patchguard.sqlite3"
    init_database(ROOT, db_path)

    catalog_root = tmp_path / "project"
    shutil.copytree(FIXTURE / "catalog", catalog_root / "catalog")

    connection = connect(db_path)
    try:
        result = seed_from_catalog(catalog_root, connection)
        assert result["applications"] == 1
        assert result["sources"] == 1
        assert result["patches"] == 1
        assert result["attribution"] == 1
        assert result["compatibility"] == 1

        patch = connection.execute("SELECT * FROM patches WHERE slug = ?", ("com.example.app/remove-ads",)).fetchone()
        assert patch["runtime_tested"] == 0
        assert patch["apk_tested"] == 0
        assert patch["compatibility_runtime_verified"] == 0
        assert patch["audit_scope"] == "SOURCE_CODE_ONLY"
        assert patch["distribution_status"] == "NOT_ELIGIBLE"
    finally:
        connection.close()
