"""Pydantic schema definitions for all booking types.

This module defines validated data models for each travel service
type supported by the multi-agent system. Each schema enforces
type safety and data validation at the boundary.
"""

from pydantic import BaseModel, Field  # Data validation framework


class TravelRequest(BaseModel):
    """Schema representing a user's travel booking request.

    Captures the essential details needed to route the request
    to the appropriate specialized booking agents.
    """

    # The city or region the traveler is departing from
    origin: str = Field(description="Departure city or location")

    # The city or region the traveler wants to reach
    destination: str = Field(description="Arrival city or location")

    # Travel start date in ISO format (YYYY-MM-DD)
    departure_date: str = Field(description="Departure date in YYYY-MM-DD")

    # Travel return date in ISO format, optional for one-way trips
    return_date: str | None = Field(
        default=None, description="Return date in YYYY-MM-DD, optional"
    )

    # Number of travelers for the booking
    num_travelers: int = Field(default=1, ge=1, le=20, description="Traveler count")

    # Maximum budget in USD for the entire trip
    budget: float | None = Field(
        default=None, ge=0, description="Maximum budget in USD"
    )

    # Free-text preferences or special requirements
    preferences: str = Field(
        default="", description="Additional preferences or requirements"
    )


class FlightBooking(BaseModel):
    """Schema for a confirmed or proposed flight booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique flight booking reference")

    # Name of the airline operating the flight
    airline: str = Field(description="Operating airline name")

    # Flight number for identification
    flight_number: str = Field(description="Airline flight number")

    # Departure airport or city name
    origin: str = Field(description="Departure airport or city")

    # Arrival airport or city name
    destination: str = Field(description="Arrival airport or city")

    # Scheduled departure date and time
    departure_time: str = Field(description="Departure datetime")

    # Scheduled arrival date and time
    arrival_time: str = Field(description="Arrival datetime")

    # Total price in USD for all passengers
    price: float = Field(ge=0, description="Total price in USD")

    # Booking status indicator
    status: str = Field(default="confirmed", description="Booking status")


class HotelBooking(BaseModel):
    """Schema for a confirmed or proposed hotel booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique hotel booking reference")

    # Name of the hotel property
    hotel_name: str = Field(description="Hotel property name")

    # Physical address of the hotel
    address: str = Field(description="Hotel street address")

    # Date of guest check-in
    check_in_date: str = Field(description="Check-in date YYYY-MM-DD")

    # Date of guest check-out
    check_out_date: str = Field(description="Check-out date YYYY-MM-DD")

    # Type of room booked (e.g., Standard, Deluxe, Suite)
    room_type: str = Field(description="Room category or type")

    # Total price in USD for the entire stay
    price_per_night: float = Field(ge=0, description="Nightly rate in USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")


class CarRentalBooking(BaseModel):
    """Schema for a confirmed or proposed car rental booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique rental booking reference")

    # Car rental company name
    company: str = Field(description="Rental company name")

    # Type of vehicle reserved
    vehicle_type: str = Field(description="Vehicle category")

    # Pickup location address or name
    pickup_location: str = Field(description="Vehicle pickup location")

    # Vehicle return location address or name
    dropoff_location: str = Field(description="Vehicle return location")

    # Rental start date
    pickup_date: str = Field(description="Pickup date YYYY-MM-DD")

    # Rental end date
    dropoff_date: str = Field(description="Return date YYYY-MM-DD")

    # Daily rental rate in USD
    daily_rate: float = Field(ge=0, description="Daily rate in USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")


class BusBooking(BaseModel):
    """Schema for a confirmed or proposed bus booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique bus booking reference")

    # Bus service operator name
    operator: str = Field(description="Bus service operator")

    # Route identification number or name
    route: str = Field(description="Bus route identifier")

    # Departure station or stop
    origin: str = Field(description="Departure station")

    # Arrival station or stop
    destination: str = Field(description="Arrival station")

    # Scheduled departure date and time
    departure_time: str = Field(description="Departure datetime")

    # Expected arrival date and time
    arrival_time: str = Field(description="Arrival datetime")

    # Ticket price in USD per passenger
    price: float = Field(ge=0, description="Ticket price in USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")


class TrainBooking(BaseModel):
    """Schema for a confirmed or proposed train booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique train booking reference")

    # Railway operator name
    operator: str = Field(description="Railway operator name")

    # Train service number
    train_number: str = Field(description="Train service number")

    # Departure station name
    origin: str = Field(description="Departure station")

    # Arrival station name
    destination: str = Field(description="Arrival station")

    # Scheduled departure date and time
    departure_time: str = Field(description="Departure datetime")

    # Expected arrival date and time
    arrival_time: str = Field(description="Arrival datetime")

    # Travel class (Economy, Business, First)
    travel_class: str = Field(default="Economy", description="Travel class")

    # Ticket price in USD per passenger
    price: float = Field(ge=0, description="Ticket price in USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")


class TourPackageBooking(BaseModel):
    """Schema for a confirmed or proposed tour package booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique tour booking reference")

    # Tour package descriptive name
    package_name: str = Field(description="Tour package name")

    # Tour operator or agency name
    operator: str = Field(description="Tour operator name")

    # Duration of the tour in days
    duration_days: int = Field(ge=1, description="Tour duration in days")

    # List of destinations or stops on the tour
    destinations: list[str] = Field(description="Tour destinations list")

    # What is included in the package (meals, transport, etc.)
    inclusions: list[str] = Field(description="Package inclusions")

    # Total price in USD per person
    price_per_person: float = Field(ge=0, description="Price per person USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")


class SightseeingBooking(BaseModel):
    """Schema for a confirmed or proposed sightseeing activity booking."""

    # Unique booking reference identifier
    booking_id: str = Field(description="Unique activity booking reference")

    # Name of the sightseeing activity or attraction
    activity_name: str = Field(description="Activity or attraction name")

    # Activity provider or venue name
    provider: str = Field(description="Activity provider name")

    # Location of the activity
    location: str = Field(description="Activity location")

    # Scheduled date for the activity
    date: str = Field(description="Activity date YYYY-MM-DD")

    # Duration of the activity in hours
    duration_hours: float = Field(ge=0.5, description="Duration in hours")

    # Price per person in USD
    price_per_person: float = Field(ge=0, description="Price per person USD")

    # Booking confirmation status
    status: str = Field(default="confirmed", description="Booking status")
