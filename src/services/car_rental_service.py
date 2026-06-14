"""Car rental service providing search and reservation capabilities.

This module simulates integration with an external car rental API,
returning mock data for demonstration purposes.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class CarRentalService(BaseService):
    """Service for searching and booking rental vehicles."""

    def __init__(self) -> None:
        """Initialize the car rental booking service."""
        super().__init__("car_rental")

    def search(
        self,
        pickup_location: str,
        pickup_date: str,
        dropoff_date: str,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available rental vehicles at a location.

        Args:
            pickup_location: Vehicle pickup city or address.
            pickup_date: Rental start date YYYY-MM-DD.
            dropoff_date: Rental end date YYYY-MM-DD.
            **kwargs: Additional filters (vehicle type, etc.).

        Returns:
            List of available rental vehicle options.
        """
        self._logger.info(
            "Searching car rentals in %s: %s to %s",
            pickup_location, pickup_date, dropoff_date,
        )

        return [
            {
                "company": "DriveEasy Rentals",
                "vehicle_type": "Economy Sedan",
                "pickup_location": pickup_location,
                "dropoff_location": pickup_location,
                "pickup_date": pickup_date,
                "dropoff_date": dropoff_date,
                "daily_rate": 45.00,
            },
            {
                "company": "Premium Auto Hire",
                "vehicle_type": "SUV",
                "pickup_location": pickup_location,
                "dropoff_location": pickup_location,
                "pickup_date": pickup_date,
                "dropoff_date": dropoff_date,
                "daily_rate": 85.00,
            },
        ]

    def book(self, **kwargs: Any) -> dict[str, Any]:
        """Book a rental vehicle and return confirmation.

        Args:
            **kwargs: Booking parameters including vehicle and dates.

        Returns:
            Dictionary with booking confirmation details.
        """
        booking_id = self._generate_booking_id("CAR")
        self._logger.info("Booking car rental, ID: %s", booking_id)

        return {
            "booking_id": booking_id,
            "company": kwargs.get("company", "Unknown"),
            "vehicle_type": kwargs.get("vehicle_type", "Standard"),
            "pickup_location": kwargs.get("pickup_location", ""),
            "dropoff_location": kwargs.get("dropoff_location", ""),
            "pickup_date": kwargs.get("pickup_date", ""),
            "dropoff_date": kwargs.get("dropoff_date", ""),
            "daily_rate": kwargs.get("daily_rate", 0.0),
            "status": "confirmed",
        }
