"""Hotel booking service providing search and reservation capabilities.

This module simulates integration with an external hotel booking API,
returning mock data for demonstration purposes.
"""

from typing import Any  # Generic type annotation

from src.services.base_service import BaseService  # Base service class


class HotelService(BaseService):
    """Service for searching and booking hotel accommodations."""

    def __init__(self) -> None:
        """Initialize the hotel booking service."""
        # Call parent constructor with the service identifier
        super().__init__("hotel")

    def search(
        self,
        destination: str,
        check_in_date: str,
        check_out_date: str,
        num_guests: int = 1,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Search for available hotels at the destination.

        Args:
            destination: City or area to search for hotels.
            check_in_date: Check-in date in YYYY-MM-DD format.
            check_out_date: Check-out date in YYYY-MM-DD format.
            num_guests: Number of guests for the booking.
            **kwargs: Additional optional search filters.

        Returns:
            List of available hotel options with pricing.
        """
        # Log the hotel search request
        self._logger.info(
            "Searching hotels in %s: %s to %s for %d guests",
            destination, check_in_date, check_out_date, num_guests,
        )

        # Return simulated hotel search results
        return [
            {
                "hotel_name": "Grand Plaza Hotel",
                "address": f"123 Main Street, {destination}",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "room_type": "Deluxe Double",
                "price_per_night": 180.00,
                "rating": 4.5,
            },
            {
                "hotel_name": "Comfort Inn Express",
                "address": f"456 Park Avenue, {destination}",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "room_type": "Standard Queen",
                "price_per_night": 120.00,
                "rating": 4.0,
            },
            {
                "hotel_name": "Luxury Suites International",
                "address": f"789 Ocean Drive, {destination}",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "room_type": "Executive Suite",
                "price_per_night": 350.00,
                "rating": 4.8,
            },
        ]

    def book(
        self,
        hotel_name: str,
        address: str,
        check_in_date: str,
        check_out_date: str,
        room_type: str,
        price_per_night: float,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Book a hotel room and return confirmation details.

        Args:
            hotel_name: Name of the hotel to book.
            address: Hotel address.
            check_in_date: Guest check-in date.
            check_out_date: Guest check-out date.
            room_type: Type of room to reserve.
            price_per_night: Nightly rate for the room.
            **kwargs: Additional booking options.

        Returns:
            Dictionary with booking confirmation details.
        """
        # Generate a unique booking reference for this reservation
        booking_id = self._generate_booking_id("HTL")

        # Log the booking creation
        self._logger.info(
            "Booking hotel %s in room %s, ID: %s",
            hotel_name, room_type, booking_id,
        )

        # Return the structured booking confirmation
        return {
            "booking_id": booking_id,
            "hotel_name": hotel_name,
            "address": address,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "room_type": room_type,
            "price_per_night": price_per_night,
            "status": "confirmed",
        }
