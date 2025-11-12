"""Module for reading configuration files."""

from pathlib import Path
import yaml
from logger import get_logger

logger = get_logger(__name__)


def load_config(config_path: str) -> dict:
    """
    Load configuration from a YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    config_path = Path(config_path)
    if not config_path.is_file():
        logger.error(f"Configuration file not found: {config_path}")
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    elif not config_path.suffix == ".yaml":
        logger.error(f"Invalid configuration file format: {config_path.suffix}")
        raise ValueError(f"Invalid configuration file format: {config_path.suffix}")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        logger.info(f"Configuration loaded from {config_path}")
    return config
