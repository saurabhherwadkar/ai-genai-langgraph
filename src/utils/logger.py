"""Centralized logging configuration module.

This module provides a factory function for creating consistently configured
loggers throughout the application. Log level is configurable via the
settings YAML file or the LOG_LEVEL environment variable.
"""

import logging  # Standard library logging framework
import os  # Operating system interface for environment variables
import sys  # System-specific parameters for stdout stream
from logging.handlers import RotatingFileHandler  # File rotation handler
from pathlib import Path  # Object-oriented filesystem path handling

# Define the project root directory for log file placement
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Map string log level names to logging module constants
LOG_LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,  # Detailed diagnostic information
    "INFO": logging.INFO,  # Confirmation of expected behavior
    "WARNING": logging.WARNING,  # Indication of potential issues
    "ERROR": logging.ERROR,  # Serious problem that needs attention
    "CRITICAL": logging.CRITICAL,  # Program may not continue
}

# Track whether the logging system has been initialized
_logging_initialized: bool = False


def _get_log_level() -> int:
    """Determine the active log level from environment or default.

    Checks the LOG_LEVEL environment variable first, then falls back
    to INFO as the default level.

    Returns:
        Integer log level constant from the logging module.
    """
    # Read log level from environment variable with INFO fallback
    level_name = os.environ.get("LOG_LEVEL", "INFO").upper()

    # Map the string name to logging constant, default to INFO
    return LOG_LEVEL_MAP.get(level_name, logging.INFO)


def _ensure_log_directory() -> Path:
    """Create the logs directory if it does not already exist.

    Returns:
        Path object pointing to the logs directory.
    """
    # Construct the path to the logs directory
    log_dir = PROJECT_ROOT / "logs"

    # Create the directory and any missing parents
    log_dir.mkdir(parents=True, exist_ok=True)

    # Return the verified directory path
    return log_dir


def _initialize_logging() -> None:
    """Set up the root logger with console and file handlers.

    Configures both a console handler for immediate output and a
    rotating file handler for persistent log storage. This function
    is idempotent and only runs once.
    """
    # Use module-level flag to prevent duplicate initialization
    global _logging_initialized

    # Skip if already configured to avoid duplicate handlers
    if _logging_initialized:
        return

    # Determine the active log level for all handlers
    log_level = _get_log_level()

    # Define the standard log message format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Define the timestamp format for log entries
    date_format = "%Y-%m-%d %H:%M:%S"

    # Create the log formatter instance
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # Configure the root logger with the determined level
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create and configure the console output handler
    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(log_level)  # Apply same level as root
    console_handler.setFormatter(formatter)  # Apply standard format
    root_logger.addHandler(console_handler)  # Attach to root logger

    # Create the log file directory structure
    log_dir = _ensure_log_directory()

    # Define the log file path within the logs directory
    log_file = log_dir / "travel_agent.log"

    # Create rotating file handler with size limit and backup count
    file_handler = RotatingFileHandler(
        filename=str(log_file),  # Path to the log file
        maxBytes=10 * 1024 * 1024,  # 10 MB maximum file size
        backupCount=5,  # Keep 5 rotated backup files
        encoding="utf-8",  # Use UTF-8 text encoding
    )
    file_handler.setLevel(log_level)  # Apply same level as root
    file_handler.setFormatter(formatter)  # Apply standard format
    root_logger.addHandler(file_handler)  # Attach to root logger

    # Mark logging as initialized to prevent re-entry
    _logging_initialized = True


def get_logger(name: str) -> logging.Logger:
    """Create or retrieve a named logger instance.

    This is the primary interface for obtaining loggers. It ensures
    the logging system is initialized before returning the logger.

    Args:
        name: The hierarchical name for the logger, typically __name__.

    Returns:
        Configured Logger instance ready for use.
    """
    # Ensure the logging infrastructure is set up
    _initialize_logging()

    # Return a named child logger from the hierarchy
    return logging.getLogger(name)
