"""Base service class providing common functionality for all booking services.

This module defines the abstract base for all travel service integrations,
providing shared logic for ID generation, error handling, and configuration.
"""

import uuid  # Universally unique identifier generation
from abc import ABC, abstractmethod  # Abstract base class support
from typing import Any  # Generic type annotation

from src.utils.logger import get_logger  # Application logger factory

# Initialize module-level logger for the base service
logger = get_logger(__name__)


class BaseService(ABC):
    """Abstract base class for all travel booking service integrations.

    Provides common utilities such as unique ID generation and
    standardized error handling that all concrete services inherit.
    """

    def __init__(self, service_name: str) -> None:
        """Initialize the base service with a descriptive name.

        Args:
            service_name: Human-readable name identifying this service.
        """
        # Store the service name for logging and identification
        self._service_name = service_name

        # Create a service-specific logger instance
        self._logger = get_logger(f"service.{service_name}")

        # Log service initialization for debugging
        self._logger.info("Initialized %s service", service_name)

    def _generate_booking_id(self, prefix: str) -> str:
        """Generate a unique booking reference ID with a service prefix.

        Creates a short unique identifier by combining a service prefix
        with a truncated UUID for human readability.

        Args:
            prefix: Short prefix identifying the service type (e.g., FLT, HTL).

        Returns:
            Formatted booking ID string like 'FLT-a1b2c3d4'.
        """
        # Generate a UUID and take the first 8 characters for brevity
        unique_part = uuid.uuid4().hex[:8]

        # Combine prefix and unique portion with a hyphen separator
        booking_id = f"{prefix}-{unique_part}"

        # Log the generated booking ID for audit trail
        self._logger.debug("Generated booking ID: %s", booking_id)

        # Return the formatted booking reference
        return booking_id

    @abstractmethod
    def search(self, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for available options matching the given criteria.

        Must be implemented by each concrete service to provide
        service-specific search functionality.

        Args:
            **kwargs: Service-specific search parameters.

        Returns:
            List of matching options as dictionaries.
        """
        ...  # pragma: no cover

    @abstractmethod
    def book(self, **kwargs: Any) -> dict[str, Any]:
        """Create a booking for the selected option.

        Must be implemented by each concrete service to handle
        service-specific booking logic.

        Args:
            **kwargs: Service-specific booking parameters.

        Returns:
            Dictionary containing booking confirmation details.
        """
        ...  # pragma: no cover
