"""
Application-wide logging configuration.
Logs to console and to a rotating file under storage/logs/.
"""
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "storage/logs"
os.makedirs(LOG_DIR, exist_ok=True)


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("defect_detection")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler(
        f"{LOG_DIR}/app.log", maxBytes=5_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


logger = setup_logging()
