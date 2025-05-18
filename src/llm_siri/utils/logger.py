import os
import sys

from loguru import logger


def get_logger():
    return logger


def setup_logger():
    logger.remove()
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logger.add(sink=sys.stdout, level=level)
