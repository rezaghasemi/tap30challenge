"""
Get a logger instance with the specified name.

Returns:
    logging.Logger: A logger instance with the specified name.

"""

import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / f"log_{datetime.now().strftime('%Y-%m-%d')}.log"

logging.basicConfig(
    filename=LOG_FILE,
    format="[%(asctime)s] - %[(name)]s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)
