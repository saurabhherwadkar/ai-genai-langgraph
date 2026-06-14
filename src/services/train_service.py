"""Train booking service providing search and reservation capabilities.

This module simulates integration with an external railway booking API.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class TrainService(BaseService):
    """Service for searching and booking train travel."""

    def __init__(self) -> None:
        """Initialize the train booking service."""
        super().__init__("train")

    def search(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        travel_class: str = "Economy",
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available train services between stations.

        Args:
            origin: Departure station.
            destination: Arrival station.
            departure_date: Travel date YYYY-MM-DD.
            travel_class: Preferred class of travel.
            **kwargs: Additional search filters.

        Returns:
            List of available train service options.
        """
        self._logger.info(
            "Searching trains: %s -> %s on %s (%s class)",
            origin, destination, departure_date, travel_class,
        )

        return [
            {
                "operator": "RailConnect",
                "train_number": "RC-1042",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T06:30:00",
                "arrival_time": f"{departure_date}T09:45:00",
                "travel_class": travel_class,
                "price": 75.00,
            },
            {
                "operator": "SpeedRail",
                "train_number": "SR-2201",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T10:00:00",
                "arrival_time": f"{departure_date}T12:30:00",
                "travel_class": travel_class,
                "price": 110.00,
            },
        ]

    def book(self, **kwargs: Any) -> dict[str, Any]:
        """Book a train ticket and return confirmation.

        Args:
            **kwargs: Booking parameters including train and class.

        Returns:
            Dictionary with booking confirmation details.
        """
        booking_id = self._generate_booking_id("TRN")
        self._logger.info("Booking train ticket, ID: %s", booking_id)

        return {
            "booking_id": booking_id,
            "operator": kwargs.get("operator", "Unknown"),
            "train_number": kwargs.get("train_number", ""),
            "origin": kwargs.get("origin", ""),
            "destination": kwargs.get("destination", ""),
            "departure_time": kwargs.get("departure_time", ""),
            "arrival_time": kwargs.get("arrival_time", ""),
            "travel_class": kwargs.get("travel_class", "Economy"),
            "price": kwargs.get("price", 0.0),
            "status": "confirmed",
        }
