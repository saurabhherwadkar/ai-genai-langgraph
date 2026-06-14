"""Input sanitization module for security vulnerability protection.

This module provides functions to validate and sanitize user inputs
to prevent injection attacks and ensure data integrity throughout
the application.
"""

import re  # Regular expression module for pattern matching
from typing import Any  # Type hint for generic values

from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger instance
logger = get_logger(__name__)

# Maximum allowed input string length to prevent buffer overflow
MAX_INPUT_LENGTH: int = 5000

# Pattern to detect potential injection characters
INJECTION_PATTERN: re.Pattern = re.compile(r"[<>{};\|\$`]")

# Pattern for valid location names (letters, spaces, hyphens, commas)
VALID_LOCATION_PATTERN: re.Pattern = re.compile(
    r"^[a-zA-Z\s,.\-']+$"
)

# Pattern for valid date format (YYYY-MM-DD)
VALID_DATE_PATTERN: re.Pattern = re.compile(
    r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"
)


def sanitize_string(value: str) -> str:
    """Remove potentially dangerous characters from input strings.

    Strips leading/trailing whitespace and removes characters that
    could be used for injection attacks.

    Args:
        value: The raw input string to sanitize.

    Returns:
        Cleaned string with dangerous characters removed.

    Raises:
        ValueError: When input exceeds maximum allowed length.
    """
    # Check that input does not exceed maximum length
    if len(value) > MAX_INPUT_LENGTH:
        logger.warning("Input exceeds maximum length of %d", MAX_INPUT_LENGTH)
        raise ValueError(
            f"Input exceeds maximum length of {MAX_INPUT_LENGTH} characters"
        )

    # Strip leading and trailing whitespace from the input
    cleaned = value.strip()

    # Remove any characters matching the injection pattern
    cleaned = INJECTION_PATTERN.sub("", cleaned)

    # Log if any characters were removed during sanitization
    if cleaned != value.strip():
        logger.info("Sanitized potentially dangerous characters from input")

    # Return the sanitized string
    return cleaned


def validate_location(location: str) -> bool:
    """Validate that a location string contains only safe characters.

    Checks the location against an allowlist pattern of characters
    typically found in city and country names.

    Args:
        location: The location string to validate.

    Returns:
        True if the location matches the valid pattern, False otherwise.
    """
    # Check if location matches the allowed character pattern
    is_valid = bool(VALID_LOCATION_PATTERN.match(location))

    # Log validation failures for monitoring
    if not is_valid:
        logger.warning("Invalid location format detected: %s", location[:50])

    # Return the validation result
    return is_valid


def validate_date(date_string: str) -> bool:
    """Validate that a date string matches the expected ISO format.

    Ensures the date is in YYYY-MM-DD format with valid month and
    day ranges.

    Args:
        date_string: The date string to validate.

    Returns:
        True if the date matches ISO format, False otherwise.
    """
    # Check if date matches the YYYY-MM-DD pattern
    is_valid = bool(VALID_DATE_PATTERN.match(date_string))

    # Log validation failures for monitoring
    if not is_valid:
        logger.warning("Invalid date format: %s", date_string[:20])

    # Return the validation result
    return is_valid


def validate_positive_integer(value: Any) -> bool:
    """Validate that a value is a positive integer.

    Useful for validating passenger counts, quantities, and other
    numeric fields that must be positive.

    Args:
        value: The value to validate as a positive integer.

    Returns:
        True if value is a positive integer, False otherwise.
    """
    # Attempt to verify the value is a positive integer
    try:
        # Convert and check positivity
        return isinstance(value, int) and value > 0
    except (TypeError, ValueError):
        # Return False for any conversion failures
        return False
