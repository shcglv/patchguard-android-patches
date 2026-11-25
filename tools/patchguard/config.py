"""Configuration loading for PatchGuard.

The repository is the source of truth. This module only resolves paths and
loads the public, non-secret YAML configuration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class ConfigError(RuntimeError):
    """Raised when the project configuration cannot be loaded."""


def find_project_root(start: Path | None = None) -> Path:
    """Find the repository root by looking for pyproject.toml and config/settings.yml."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / "config" / "settings.yml").is_file():
            return candidate
    raise ConfigError(
        "Could not find the PatchGuard project root. Run from the repository root "
        "or pass --root."
    )


def load_yaml(path: Path) -> Any:
    """Load a UTF-8 YAML file, raising ConfigError with context on failure."""
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except FileNotFoundError as exc:
        raise ConfigError(f"Configuration file not found: {path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML in {path}: {exc}") from exc


def load_config(root: Path | None = None) -> dict[str, Any]:
    """Load config/settings.yml and resolve project paths."""
    project_root = (root or find_project_root()).resolve()
    settings = load_yaml(project_root / "config" / "settings.yml")
    if not isinstance(settings, dict):
        raise ConfigError("config/settings.yml must contain a mapping")
    settings = dict(settings)
    settings["_root"] = str(project_root)
    return settings


def resolve_path(config: dict[str, Any], value: str | None) -> Path | None:
    """Resolve a configured path relative to the repository root.

    Absolute paths (including Windows drive paths) are preserved.
    """
    if not value:
        return None
    path = Path(value).expanduser()
    if path.is_absolute() or (len(value) > 1 and value[1] == ":"):
        return path
    return Path(config["_root"]) / path


def path_for(config: dict[str, Any], key: str) -> Path | None:
    """Return a path from the settings.paths mapping."""
    paths = config.get("paths") or {}
    return resolve_path(config, paths.get(key))


def project_name(config: dict[str, Any]) -> str:
    project = config.get("project") or {}
    return str(project.get("name") or "PatchGuard Android Patches")
