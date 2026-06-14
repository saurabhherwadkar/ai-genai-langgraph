"""Bus booking service providing search and reservation capabilities.

This module simulates integration with an external bus service API.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class BusService(BaseService):
    """Service for searching and booking bus travel."""

    def __init__(self) -> None:
        """Initialize the bus booking service."""
        super().__init__("bus")

    def search(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available bus routes between locations.

        Args:
            origin: Departure station or city.
            destination: Arrival station or city.
            departure_date: Travel date YYYY-MM-DD.
            **kwargs: Additional search filters.

        Returns:
            List of available bus route options.
        """
        self._logger.info(
            "Searching bus routes: %s -> %s on %s",
            origin, destination, departure_date,
        )

        return [
            {
                "operator": "National Express",
                "route": f"{origin}-{destination}-Express",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T07:00:00",
                "arrival_time": f"{departure_date}T11:30:00",
                "price": 35.00,
            },
            {
                "operator": "GreenLine Coaches",
                "route": f"{origin}-{destination}-Standard",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T09:30:00",
                "arrival_time": f"{departure_date}T14:00:00",
                "price": 25.00,
            },
        ]

    def book(self, **kwargs: Any) -> dict[str, Any]:
        """Book a bus ticket and return confirmation.

        Args:
            **kwargs: Booking parameters including route and date.

        Returns:
            Dictionary with booking confirmation details.
        """
        booking_id = self._generate_booking_id("BUS")
        self._logger.info("Booking bus ticket, ID: %s", booking_id)

        return {
            "booking_id": booking_id,
            "operator": kwargs.get("operator", "Unknown"),
            "route": kwargs.get("route", ""),
            "origin": kwargs.get("origin", ""),
            "destination": kwargs.get("destination", ""),
            "departure_time": kwargs.get("departure_time", ""),
            "arrival_time": kwargs.get("arrival_time", ""),
            "price": kwargs.get("price", 0.0),
            "status": "confirmed",
        }
