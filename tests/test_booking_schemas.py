"""Unit tests for booking schema validation."""

import pytest  # Test framework
from pydantic import ValidationError  # Pydantic validation errors

from src.models.booking_schemas import (  # Schemas under test
    FlightBooking,
    HotelBooking,
    TravelRequest,
)


class TestTravelRequest:
    """Test suite for the TravelRequest schema."""

    def test_valid_request(self) -> None:
        """Verify a complete valid request passes validation."""
        request = TravelRequest(
            origin="New York",
            destination="London",
            departure_date="2025-03-15",
            num_travelers=2,
            budget=5000.0,
        )
        assert request.origin == "New York"
        assert request.num_travelers == 2

    def test_minimal_request(self) -> None:
        """Verify a minimal request with defaults passes."""
        request = TravelRequest(
            origin="NYC",
            destination="LAX",
            departure_date="2025-04-01",
        )
        assert request.num_travelers == 1
        assert request.return_date is None

    def test_invalid_traveler_count_zero(self) -> None:
        """Verify zero travelers fails validation."""
        with pytest.raises(ValidationError):
            TravelRequest(
                origin="NYC",
                destination="LAX",
                departure_date="2025-04-01",
                num_travelers=0,
            )

    def test_invalid_traveler_count_too_high(self) -> None:
        """Verify more than 20 travelers fails validation."""
        with pytest.raises(ValidationError):
            TravelRequest(
                origin="NYC",
                destination="LAX",
                departure_date="2025-04-01",
                num_travelers=21,
            )

    def test_negative_budget_fails(self) -> None:
        """Verify negative budget fails validation."""
        with pytest.raises(ValidationError):
            TravelRequest(
                origin="NYC",
                destination="LAX",
                departure_date="2025-04-01",
                budget=-100.0,
            )


class TestFlightBooking:
    """Test suite for the FlightBooking schema."""

    def test_valid_booking(self) -> None:
        """Verify a complete valid booking passes validation."""
        booking = FlightBooking(
            booking_id="FLT-abc12345",
            airline="TestAir",
            flight_number="TA-100",
            origin="NYC",
            destination="LON",
            departure_time="2025-03-15T08:00:00",
            arrival_time="2025-03-15T20:00:00",
            price=450.0,
        )
        assert booking.status == "confirmed"

    def test_negative_price_fails(self) -> None:
        """Verify negative price fails validation."""
        with pytest.raises(ValidationError):
            FlightBooking(
                booking_id="FLT-abc12345",
                airline="TestAir",
                flight_number="TA-100",
                origin="NYC",
                destination="LON",
                departure_time="2025-03-15T08:00:00",
                arrival_time="2025-03-15T20:00:00",
                price=-50.0,
            )


class TestHotelBooking:
    """Test suite for the HotelBooking schema."""

    def test_valid_booking(self) -> None:
        """Verify a complete valid hotel booking passes validation."""
        booking = HotelBooking(
            booking_id="HTL-xyz98765",
            hotel_name="Grand Hotel",
            address="123 Main St",
            check_in_date="2025-03-15",
            check_out_date="2025-03-20",
            room_type="Deluxe",
            price_per_night=200.0,
        )
        assert booking.status == "confirmed"
        assert booking.price_per_night == 200.0
