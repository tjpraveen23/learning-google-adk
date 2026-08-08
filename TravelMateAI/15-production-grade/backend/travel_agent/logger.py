"""
==============================================================
Day 15 - Production Multi-Agent
Step 3: Structured Logging

FILE_LOG_ENTRY=yes  - write logs to logs/log.txt
FILE_LOG_ENTRY=no   - print logs to console

Features:
- Timestamp
- Log level
- Logger name
- Request ID
- Configurable output
==============================================================
"""

import logging
import sys
from pathlib import Path
from contextvars import ContextVar

from .config import Settings

# ---------------------------------------------------------
# Request ID context
# ---------------------------------------------------------

request_id_var: ContextVar[str] = ContextVar(
    "request_id",
    default="-"
)

# ---------------------------------------------------------
# Custom formatter
# ---------------------------------------------------------

class RequestFormatter(logging.Formatter):

    def format(self, record):

        record.request_id = request_id_var.get()

        return super().format(record)

# ---------------------------------------------------------
# Logger factory
# ---------------------------------------------------------

def get_logger(name: str):

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = RequestFormatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(request_id)s | %(message)s"
    )

    # -----------------------------------------------------
    # Console or File based on configuration
    # -----------------------------------------------------

    if Settings.FILE_LOG_ENTRY.lower() == "yes":

        Path("logs").mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            Settings.LOG_DIR / "travelmate.log",
            encoding="utf-8"
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    else:

        console = logging.StreamHandler(sys.stdout)

        console.setFormatter(formatter)

        logger.addHandler(console)

    logger.propagate = False

    return logger

# ---------------------------------------------------------
# Request ID helper
# ---------------------------------------------------------

def set_request_id(request_id: str):

    request_id_var.set(request_id)