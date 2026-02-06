import logging
import logging.config
import json
from datetime import datetime
from typing import Dict, Any

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, "user_id"):
            log_entry["user_id"] = record.user_id
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        if hasattr(record, "ip_address"):
            log_entry["ip_address"] = record.ip_address
        if hasattr(record, "extra"):
            log_entry["extra"] = record.extra

        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def setup_logging():
    """Setup structured logging configuration."""

    # Define logging configuration
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JSONFormatter,
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": settings.log_level,
                "formatter": "json" if settings.log_format == "json" else "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": settings.log_level,
                "formatter": "json" if settings.log_format == "json" else "standard",
                "filename": "logs/app.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {  # Root logger
                "handlers": ["console"],
                "level": settings.log_level,
                "propagate": False,
            },
            "app": {
                "handlers": ["console", "file"],
                "level": settings.log_level,
                "propagate": False,
            },
            "uvicorn": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": False,
            },
            "sqlalchemy.engine": {
                "handlers": ["console"] if settings.debug else [],
                "level": "INFO" if settings.debug else "WARNING",
                "propagate": False,
            },
        },
    }

    # Create logs directory if it doesn't exist
    import os

    os.makedirs("logs", exist_ok=True)

    # Apply configuration
    logging.config.dictConfig(config)


def get_logger(name: str) -> logging.Logger:
    """Get logger with specified name."""
    return logging.getLogger(name)
