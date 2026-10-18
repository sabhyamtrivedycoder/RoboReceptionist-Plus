"""
core/logging_config.py - Enterprise Structured Logging Setup
"""

import sys
import logging
from logging.config import dictConfig

def configure_logging(level: str = "INFO"):
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "clinical": {
                "format": "[%(asctime)s] [ER-TELEMETRY] [%(levelname)s] %(name)s -> %(message)s",
                "datefmt": "%H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "clinical",
                "stream": sys.stdout,
                "level": level
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": level,
                "propagate": True
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn.access": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            }
        }
    }
    dictConfig(log_config)

logger = logging.getLogger("robo.receptionist")
