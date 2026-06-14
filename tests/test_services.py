"""Unit tests for the booking service modules."""

import pytest  # Test framework

from src.services.bus_service import BusService  # Bus service under test
from src.services.car_rental_service import CarRentalService  # Car service
from src.services.flight_service import FlightService  # Flight service
from src.services.hotel_service import HotelService  # Hotel service
from src.services.sightseeing_service import SightseeingService  # Activity service
from src.services.tour_service import TourService  # Tour service
from src.services.train_service import TrainService  # Train service


class TestFlightService:
    """Test suite for the FlightService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = FlightService()

    def test_search_returns_results(self) -> None:
        """Verify flight search returns a non-empty list."""
        results = self.service.search(
            origin="NYC", destination="LON", departure_date="2025-03-15"
        )
        assert len(results) > 0

    def test_search_results_have_required_fields(self) -> None:
        """Verify each search result contains required booking fields."""
        results = self.service.search(
            origin="NYC", destination="LON", departure_date="2025-03-15"
        )
        for result in results:
            assert "airline" in result
            assert "flight_number" in result
            assert "price" in result

    def test_book_returns_confirmation(self) -> None:
        """Verify booking returns a confirmation with booking ID."""
        result = self.service.book(
            flight_number="SW-201",
            origin="NYC",
            destination="LON",
            departure_time="2025-03-15T08:00:00",
            arrival_time="2025-03-15T12:30:00",
            price=450.0,
            airline="TestAir",
        )
        assert "booking_id" in result
        assert result["status"] == "confirmed"
        assert result["booking_id"].startswith("FLT-")

    def test_book_generates_unique_ids(self) -> None:
        """Verify each booking gets a unique ID."""
        params = {
            "flight_number": "SW-201",
            "origin": "NYC",
            "destination": "LON",
            "departure_time": "2025-03-15T08:00:00",
            "arrival_time": "2025-03-15T12:30:00",
            "price": 450.0,
        }
        id1 = self.service.book(**params)["booking_id"]
        id2 = self.service.book(**params)["booking_id"]
        assert id1 != id2


class TestHotelService:
    """Test suite for the HotelService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = HotelService()

    def test_search_returns_results(self) -> None:
        """Verify hotel search returns a non-empty list."""
        results = self.service.search(
            destination="London",
            check_in_date="2025-03-15",
            check_out_date="2025-03-20",
        )
        assert len(results) > 0

    def test_search_results_have_pricing(self) -> None:
        """Verify each result includes price per night."""
        results = self.service.search(
            destination="London",
            check_in_date="2025-03-15",
            check_out_date="2025-03-20",
        )
        for result in results:
            assert "price_per_night" in result
            assert result["price_per_night"] > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify hotel booking returns proper confirmation."""
        result = self.service.book(
            hotel_name="Test Hotel",
            address="123 Test St",
            check_in_date="2025-03-15",
            check_out_date="2025-03-20",
            room_type="Standard",
            price_per_night=100.0,
        )
        assert result["booking_id"].startswith("HTL-")
        assert result["status"] == "confirmed"


class TestCarRentalService:
    """Test suite for the CarRentalService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = CarRentalService()

    def test_search_returns_results(self) -> None:
        """Verify car rental search returns options."""
        results = self.service.search(
            pickup_location="London",
            pickup_date="2025-03-15",
            dropoff_date="2025-03-20",
        )
        assert len(results) > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify car rental booking produces valid confirmation."""
        result = self.service.book(
            company="TestCar", vehicle_type="SUV",
            pickup_location="London", dropoff_location="London",
            pickup_date="2025-03-15", dropoff_date="2025-03-20",
            daily_rate=85.0,
        )
        assert result["booking_id"].startswith("CAR-")


class TestBusService:
    """Test suite for the BusService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = BusService()

    def test_search_returns_results(self) -> None:
        """Verify bus search returns route options."""
        results = self.service.search(
            origin="NYC", destination="Boston", departure_date="2025-03-15"
        )
        assert len(results) > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify bus booking produces valid confirmation."""
        result = self.service.book(
            operator="TestBus", route="NYC-BOS",
            origin="NYC", destination="Boston",
            departure_time="2025-03-15T07:00:00",
            arrival_time="2025-03-15T11:30:00",
            price=35.0,
        )
        assert result["booking_id"].startswith("BUS-")


class TestTrainService:
    """Test suite for the TrainService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = TrainService()

    def test_search_returns_results(self) -> None:
        """Verify train search returns service options."""
        results = self.service.search(
            origin="London", destination="Paris", departure_date="2025-03-16"
        )
        assert len(results) > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify train booking produces valid confirmation."""
        result = self.service.book(
            operator="TestRail", train_number="TR-001",
            origin="London", destination="Paris",
            departure_time="2025-03-16T10:00:00",
            arrival_time="2025-03-16T12:30:00",
            price=110.0,
        )
        assert result["booking_id"].startswith("TRN-")


class TestTourService:
    """Test suite for the TourService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = TourService()

    def test_search_returns_results(self) -> None:
        """Verify tour search returns package options."""
        results = self.service.search(
            destination="London", departure_date="2025-03-16"
        )
        assert len(results) > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify tour booking produces valid confirmation."""
        result = self.service.book(
            package_name="Test Tour", operator="TestOp",
            duration_days=3, destinations=["London"],
            inclusions=["Hotel"], price_per_person=299.0,
        )
        assert result["booking_id"].startswith("TUR-")


class TestSightseeingService:
    """Test suite for the SightseeingService class."""

    def setup_method(self) -> None:
        """Set up a fresh service instance for each test."""
        self.service = SightseeingService()

    def test_search_returns_results(self) -> None:
        """Verify sightseeing search returns activity options."""
        results = self.service.search(location="London", date="2025-03-16")
        assert len(results) > 0

    def test_book_returns_confirmation(self) -> None:
        """Verify sightseeing booking produces valid confirmation."""
        result = self.service.book(
            activity_name="Walking Tour", provider="TestGuides",
            location="London", date="2025-03-16",
            duration_hours=3.0, price_per_person=45.0,
        )
        assert result["booking_id"].startswith("SGT-")
