"""Logging setup with basic secret redaction."""

from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

_SECRET_PATTERNS = (
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"glpat-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*\S+"),
)


class RedactSecretsFilter(logging.Filter):
    """Replace likely secret values before a record is emitted."""

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:
            return True
        redacted = message
        for pattern in _SECRET_PATTERNS:
            redacted = pattern.sub("[REDACTED]", redacted)
        if redacted != message:
            record.msg = redacted
            record.args = ()
        return True


class JsonFormatter(logging.Formatter):
    """Minimal JSON log formatter for CI and machine consumption."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(
    verbose: bool = False,
    json_logs: bool = False,
    log_file: Path | None = None,
) -> logging.Logger:
    """Configure the root logger once and return the patchguard logger."""
    logger = logging.getLogger("patchguard")
    if getattr(logger, "_patchguard_configured", False):
        return logger

    level = logging.DEBUG if verbose else logging.INFO
    logger.setLevel(level)
    logger.propagate = False

    formatter: logging.Formatter
    if json_logs:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter("%(levelname)s %(message)s")

    stream = logging.StreamHandler(sys.stderr)
    stream.setFormatter(formatter)
    stream.addFilter(RedactSecretsFilter())
    logger.addHandler(stream)

    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.addFilter(RedactSecretsFilter())
        logger.addHandler(file_handler)

    logger._patchguard_configured = True  # type: ignore[attr-defined]
    return logger
