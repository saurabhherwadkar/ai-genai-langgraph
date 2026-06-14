"""Flight booking agent responsible for searching and booking flights.

This agent handles all flight-related operations within the travel
booking workflow, interfacing with the flight service.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import FlightBooking  # Flight schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.flight_service import FlightService  # External flight API
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the flight agent
logger = get_logger(__name__)


def flight_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books flights.

    Reads the parsed request from state, searches for available
    flights, selects the best option, and creates a booking.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with flight booking results.
    """
    # Log entry into the flight agent node
    logger.info("Flight agent processing request")

    # Initialize the flight service for API interaction
    service = FlightService()

    # Extract request details from the parsed request in state
    parsed = state.get("parsed_request", {})
    raw_query = parsed.get("raw_query", "")

    try:
        # Search for available flights using extracted parameters
        results = service.search(
            origin="New York",  # Default origin for demo
            destination="London",  # Default destination for demo
            departure_date="2025-03-15",  # Default date for demo
            num_passengers=1,
        )

        # Check if any flights were found
        if not results:
            logger.warning("No flights found for the request")
            return {
                "errors": ["No flights available for the requested route"],
                "messages": [AIMessage(content="No flights found.")],
            }

        # Select the first (cheapest) available option
        selected = results[0]

        # Book the selected flight through the service
        booking_data = service.book(**selected)

        # Create a validated FlightBooking object from the response
        flight_booking = FlightBooking(**booking_data)

        # Log successful booking creation
        logger.info(
            "Flight booked: %s on %s for $%.2f",
            flight_booking.flight_number,
            flight_booking.airline,
            flight_booking.price,
        )

        # Return state update with the new booking
        return {
            "flight_bookings": [flight_booking],
            "messages": [
                AIMessage(
                    content=f"Flight booked: {flight_booking.airline} "
                    f"{flight_booking.flight_number} "
                    f"{flight_booking.origin} -> {flight_booking.destination} "
                    f"at ${flight_booking.price:.2f}"
                )
            ],
        }

    except Exception as error:
        # Log the error with full context for debugging
        logger.error("Flight booking failed: %s", str(error), exc_info=True)

        # Return error state so the workflow can continue
        return {
            "errors": [f"Flight booking error: {str(error)}"],
            "messages": [
                AIMessage(content=f"Flight booking failed: {str(error)}")
            ],
        }
