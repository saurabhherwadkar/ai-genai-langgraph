"""Sightseeing activity service providing search and booking capabilities.

This module simulates integration with a local sightseeing and activities API.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class SightseeingService(BaseService):
    """Service for searching and booking local sightseeing activities."""

    def __init__(self) -> None:
        """Initialize the sightseeing activity service."""
        super().__init__("sightseeing")

    def search(
        self,
        location: str,
        date: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available sightseeing activities at a location.

        Args:
            location: City or area to search for activities.
            date: Date for the activity YYYY-MM-DD.
            **kwargs: Additional filters (category, duration, etc.).

        Returns:
            List of available sightseeing activity options.
        """
        self._logger.info(
            "Searching sightseeing in %s on %s", location, date,
        )

        return [
            {
                "activity_name": f"{location} City Walking Tour",
                "provider": "LocalGuides Co",
                "location": location,
                "date": date,
                "duration_hours": 3.0,
                "price_per_person": 45.00,
            },
            {
                "activity_name": f"{location} Museum & Gallery Pass",
                "provider": "CulturePass",
                "location": location,
                "date": date,
                "duration_hours": 5.0,
                "price_per_person": 65.00,
            },
            {
                "activity_name": f"{location} Food & Market Tour",
                "provider": "TasteBuds Tours",
                "location": location,
                "date": date,
                "duration_hours": 4.0,
                "price_per_person": 55.00,
            },
        ]

    def book(self, **kwargs: Any) -> dict[str, Any]:
        """Book a sightseeing activity and return confirmation.

        Args:
            **kwargs: Booking parameters including activity details.

        Returns:
            Dictionary with booking confirmation details.
        """
        booking_id = self._generate_booking_id("SGT")
        self._logger.info("Booking sightseeing activity, ID: %s", booking_id)

        return {
            "booking_id": booking_id,
            "activity_name": kwargs.get("activity_name", ""),
            "provider": kwargs.get("provider", "Unknown"),
            "location": kwargs.get("location", ""),
            "date": kwargs.get("date", ""),
            "duration_hours": kwargs.get("duration_hours", 1.0),
            "price_per_person": kwargs.get("price_per_person", 0.0),
            "status": "confirmed",
        }
