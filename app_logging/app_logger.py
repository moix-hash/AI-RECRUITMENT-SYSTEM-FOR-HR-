from __future__ import annotations

import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from config.app_config import CONFIG


class AppLogger:
    """Centralized logger with rotation-ready file handlers."""

    def __init__(self, name: str, log_file: Optional[str] = None) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, CONFIG.log_level.upper(), logging.INFO))
        if not self.logger.handlers:
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
            file_path = Path(log_file or Path(__file__).resolve().parents[1] / "logs" / f"{name}.log")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(file_path, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.addFilter(SecretMaskingFilter())
            self.logger.addHandler(file_handler)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_handler.addFilter(SecretMaskingFilter())
            self.logger.addHandler(stream_handler)

    def get_logger(self) -> logging.Logger:
        return self.logger


class SecretMaskingFilter(logging.Filter):
    """Redacts common credential formats before they leave the process."""

    _pattern = re.compile(r"(?i)(api[_-]?key|secret|token|password)([=:\s]+)([^\s,;]+)")

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self._pattern.sub(r"\1\2[REDACTED]", record.msg)
        return True
