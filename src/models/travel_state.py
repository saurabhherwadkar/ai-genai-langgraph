"""LangGraph state definition for the travel booking workflow.

This module defines the shared state that flows through the multi-agent
graph. Each agent reads from and writes to this state object as the
booking workflow progresses through different stages.
"""

from typing import Annotated  # For typed dict annotations with reducers

from langgraph.graph import MessagesState  # Base state with message handling
from typing_extensions import TypedDict  # Typed dictionary support

from src.models.booking_schemas import (  # Booking schema imports
    BusBooking,
    CarRentalBooking,
    FlightBooking,
    HotelBooking,
    SightseeingBooking,
    TourPackageBooking,
    TrainBooking,
)


def _merge_list(existing: list, new: list) -> list:
    """Reducer function that appends new items to the existing list.

    Used by LangGraph's Annotated type to define how state updates
    are merged when multiple agents write to the same list field.

    Args:
        existing: The current list in state.
        new: New items to append to the list.

    Returns:
        Combined list with new items appended.
    """
    # Combine existing and new list items
    return existing + new


class TravelState(MessagesState):
    """Central state schema for the travel booking graph.

    Inherits from MessagesState to get built-in message history
    management. Extends with booking-specific fields that track
    the progress of each service agent.
    """

    # The original user query describing the travel request
    user_request: str

    # Parsed and validated travel request details
    parsed_request: dict

    # List of service types needed (flight, hotel, car, etc.)
    required_services: list[str]

    # Flight bookings accumulated by the flight agent
    flight_bookings: Annotated[list[FlightBooking], _merge_list]

    # Hotel bookings accumulated by the hotel agent
    hotel_bookings: Annotated[list[HotelBooking], _merge_list]

    # Car rental bookings accumulated by the car rental agent
    car_rental_bookings: Annotated[list[CarRentalBooking], _merge_list]

    # Bus bookings accumulated by the bus booking agent
    bus_bookings: Annotated[list[BusBooking], _merge_list]

    # Train bookings accumulated by the train booking agent
    train_bookings: Annotated[list[TrainBooking], _merge_list]

    # Tour package bookings accumulated by the tour agent
    tour_package_bookings: Annotated[list[TourPackageBooking], _merge_list]

    # Sightseeing bookings accumulated by the sightseeing agent
    sightseeing_bookings: Annotated[list[SightseeingBooking], _merge_list]

    # Error messages collected during the workflow
    errors: Annotated[list[str], _merge_list]

    # Final consolidated summary of all bookings
    final_summary: str
