"""
Logger Module

Creates log files for the AI Digitalised Document Scanner.
"""

import logging
import os

# Create logs directory if it doesn't exist
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)

LOG_FILE = os.path.join(LOG_FOLDER, "scanner.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def log_info(message):
    """
    Log an information message.
    """
    logging.info(message)


def log_warning(message):
    """
    Log a warning message.
    """
    logging.warning(message)


def log_error(message):
    """
    Log an error message.
    """
    logging.error(message)