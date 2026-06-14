"""Flight booking service providing search and reservation capabilities.

This module simulates integration with an external flight booking API,
returning mock data for demonstration purposes.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class FlightService(BaseService):
    """Service for searching and booking flight reservations."""

    def __init__(self) -> None:
        """Initialize the flight booking service."""
        # Call parent constructor with the service identifier
        super().__init__("flight")

    def search(
        self,
        origin: str,
        destination: str,
        departure_date: str,
        num_passengers: int = 1,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available flights between two locations.

        Args:
            origin: Departure city or airport code.
            destination: Arrival city or airport code.
            departure_date: Date of departure in YYYY-MM-DD format.
            num_passengers: Number of passengers traveling.
            **kwargs: Additional optional search filters.

        Returns:
            List of available flight options with pricing.
        """
        # Log the search request for monitoring and debugging
        self._logger.info(
            "Searching flights: %s -> %s on %s for %d passengers",
            origin, destination, departure_date, num_passengers,
        )

        # Return simulated flight search results
        return [
            {
                "airline": "SkyWings Airlines",
                "flight_number": "SW-201",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T08:00:00",
                "arrival_time": f"{departure_date}T12:30:00",
                "price": 450.00 * num_passengers,
                "class": "Economy",
            },
            {
                "airline": "Global Airways",
                "flight_number": "GA-445",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T14:00:00",
                "arrival_time": f"{departure_date}T18:45:00",
                "price": 520.00 * num_passengers,
                "class": "Economy",
            },
            {
                "airline": "SkyWings Airlines",
                "flight_number": "SW-305",
                "origin": origin,
                "destination": destination,
                "departure_time": f"{departure_date}T19:00:00",
                "arrival_time": f"{departure_date}T23:30:00",
                "price": 380.00 * num_passengers,
                "class": "Economy",
            },
        ]

    def book(
        self,
        flight_number: str,
        origin: str,
        destination: str,
        departure_time: str,
        arrival_time: str,
        price: float,
        airline: str = "Unknown",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Book a specific flight and return confirmation details.

        Args:
            flight_number: The flight number to book.
            origin: Departure location.
            destination: Arrival location.
            departure_time: Scheduled departure time.
            arrival_time: Scheduled arrival time.
            price: Total booking price.
            airline: Operating airline name.
            **kwargs: Additional booking options.

        Returns:
            Dictionary with booking confirmation details.
        """
        # Generate a unique booking reference for this reservation
        booking_id = self._generate_booking_id("FLT")

        # Log the booking creation for audit purposes
        self._logger.info(
            "Booking flight %s: %s -> %s, ID: %s",
            flight_number, origin, destination, booking_id,
        )

        # Return the structured booking confirmation
        return {
            "booking_id": booking_id,
            "airline": airline,
            "flight_number": flight_number,
            "origin": origin,
            "destination": destination,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "price": price,
            "status": "confirmed",
        }
