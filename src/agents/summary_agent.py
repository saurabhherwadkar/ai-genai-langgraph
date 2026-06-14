"""Summary agent responsible for aggregating all booking results.

This agent collects results from all specialized agents and produces
a consolidated travel itinerary summary for the user.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.travel_state import TravelState  # Graph state definition
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the summary agent
logger = get_logger(__name__)


def summary_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that consolidates all bookings into a summary.

    Reads all booking results from state and formats them into
    a human-readable travel itinerary summary.

    Args:
        state: Current graph state with all booking results.

    Returns:
        State update with the final consolidated summary.
    """
    # Log entry into the summary agent
    logger.info("Summary agent consolidating bookings")

    # Initialize the summary lines list
    summary_lines: list[str] = []

    # Add header to the summary
    summary_lines.append("=" * 50)
    summary_lines.append("  TRAVEL BOOKING SUMMARY")
    summary_lines.append("=" * 50)

    # Process flight bookings if any exist
    flight_bookings = state.get("flight_bookings", [])
    if flight_bookings:
        summary_lines.append("\n--- FLIGHTS ---")
        for booking in flight_bookings:
            summary_lines.append(
                f"  {booking.airline} {booking.flight_number}: "
                f"{booking.origin} -> {booking.destination}"
            )
            summary_lines.append(
                f"  Departure: {booking.departure_time} | "
                f"Price: ${booking.price:.2f}"
            )
            summary_lines.append(f"  Booking ID: {booking.booking_id}")

    # Process hotel bookings if any exist
    hotel_bookings = state.get("hotel_bookings", [])
    if hotel_bookings:
        summary_lines.append("\n--- HOTELS ---")
        for booking in hotel_bookings:
            summary_lines.append(
                f"  {booking.hotel_name} ({booking.room_type})"
            )
            summary_lines.append(
                f"  Check-in: {booking.check_in_date} | "
                f"Check-out: {booking.check_out_date}"
            )
            summary_lines.append(
                f"  Rate: ${booking.price_per_night:.2f}/night | "
                f"ID: {booking.booking_id}"
            )

    # Process car rental bookings if any exist
    car_bookings = state.get("car_rental_bookings", [])
    if car_bookings:
        summary_lines.append("\n--- CAR RENTALS ---")
        for booking in car_bookings:
            summary_lines.append(
                f"  {booking.company} - {booking.vehicle_type}"
            )
            summary_lines.append(
                f"  {booking.pickup_date} to {booking.dropoff_date} | "
                f"${booking.daily_rate:.2f}/day"
            )
            summary_lines.append(f"  Booking ID: {booking.booking_id}")

    # Process bus bookings if any exist
    bus_bookings = state.get("bus_bookings", [])
    if bus_bookings:
        summary_lines.append("\n--- BUS ---")
        for booking in bus_bookings:
            summary_lines.append(
                f"  {booking.operator}: {booking.origin} -> {booking.destination}"
            )
            summary_lines.append(
                f"  Departure: {booking.departure_time} | "
                f"Price: ${booking.price:.2f}"
            )

    # Process train bookings if any exist
    train_bookings = state.get("train_bookings", [])
    if train_bookings:
        summary_lines.append("\n--- TRAINS ---")
        for booking in train_bookings:
            summary_lines.append(
                f"  {booking.operator} {booking.train_number}: "
                f"{booking.origin} -> {booking.destination}"
            )
            summary_lines.append(
                f"  Class: {booking.travel_class} | Price: ${booking.price:.2f}"
            )

    # Process tour package bookings if any exist
    tour_bookings = state.get("tour_package_bookings", [])
    if tour_bookings:
        summary_lines.append("\n--- TOUR PACKAGES ---")
        for booking in tour_bookings:
            summary_lines.append(
                f"  {booking.package_name} by {booking.operator}"
            )
            summary_lines.append(
                f"  Duration: {booking.duration_days} days | "
                f"${booking.price_per_person:.2f}/person"
            )

    # Process sightseeing bookings if any exist
    sightseeing_bookings = state.get("sightseeing_bookings", [])
    if sightseeing_bookings:
        summary_lines.append("\n--- SIGHTSEEING ---")
        for booking in sightseeing_bookings:
            summary_lines.append(
                f"  {booking.activity_name} by {booking.provider}"
            )
            summary_lines.append(
                f"  Duration: {booking.duration_hours}h | "
                f"${booking.price_per_person:.2f}/person"
            )

    # Add errors section if any occurred during processing
    errors = state.get("errors", [])
    if errors:
        summary_lines.append("\n--- ERRORS ---")
        for error in errors:
            summary_lines.append(f"  ⚠ {error}")

    # Add footer to the summary
    summary_lines.append("\n" + "=" * 50)

    # Join all lines into the final summary string
    final_summary = "\n".join(summary_lines)

    # Log summary generation completion
    logger.info("Summary generated with %d lines", len(summary_lines))

    # Return the final summary in the state update
    return {
        "final_summary": final_summary,
        "messages": [AIMessage(content=final_summary)],
    }
