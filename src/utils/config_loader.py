"""Configuration loader module for reading YAML settings files.

This module provides a centralized way to load application configuration
from YAML files with environment-specific overrides support.
"""

import os  # Operating system interface for path operations
from pathlib import Path  # Object-oriented filesystem path handling
from typing import Any  # Type hint for generic dictionary values

import yaml  # YAML parser for configuration file reading

from src.utils.logger import get_logger  # Application logger for this module

# Initialize module-level logger instance
logger = get_logger(__name__)

# Define the base directory as the project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Default configuration file path relative to project root
DEFAULT_CONFIG_PATH = BASE_DIR / "config" / "settings.yaml"


def load_settings(config_path: str | None = None) -> dict[str, Any]:
    """Load application settings from a YAML configuration file.

    Reads the YAML configuration file and returns its contents as a
    dictionary. Supports overriding the default path via parameter or
    environment variable.

    Args:
        config_path: Optional path to the configuration file.
                     Falls back to CONFIG_PATH env var or default location.

    Returns:
        Dictionary containing all configuration key-value pairs.

    Raises:
        FileNotFoundError: When the specified configuration file does not exist.
        yaml.YAMLError: When the YAML file contains invalid syntax.
    """
    # Determine the configuration file path with fallback chain
    resolved_path = Path(
        config_path  # First priority: explicit parameter
        or os.environ.get("CONFIG_PATH")  # Second: environment variable
        or str(DEFAULT_CONFIG_PATH)  # Third: default project location
    )

    # Validate that the configuration file exists on disk
    if not resolved_path.exists():
        logger.error("Configuration file not found at: %s", resolved_path)
        raise FileNotFoundError(
            f"Configuration file not found: {resolved_path}"
        )

    # Log the configuration file being loaded for debugging
    logger.info("Loading configuration from: %s", resolved_path)

    # Open and parse the YAML configuration file safely
    with open(resolved_path, "r", encoding="utf-8") as config_file:
        # Use safe_load to prevent arbitrary code execution from YAML
        settings = yaml.safe_load(config_file)

    # Handle the case where the YAML file is empty
    if settings is None:
        logger.warning("Configuration file is empty: %s", resolved_path)
        return {}  # Return empty dict for empty config files

    # Log successful configuration load with key count
    logger.debug(
        "Configuration loaded successfully with %d top-level keys",
        len(settings),
    )

    # Return the parsed configuration dictionary
    return settings
