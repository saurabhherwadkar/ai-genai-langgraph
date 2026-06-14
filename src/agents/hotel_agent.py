"""Hotel booking agent responsible for searching and booking accommodations.

This agent handles all hotel-related operations within the travel
booking workflow, interfacing with the hotel service.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import HotelBooking  # Hotel schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.hotel_service import HotelService  # External hotel API
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the hotel agent
logger = get_logger(__name__)


def hotel_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books hotels.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with hotel booking results.
    """
    logger.info("Hotel agent processing request")

    service = HotelService()
    parsed = state.get("parsed_request", {})

    try:
        results = service.search(
            destination="London",
            check_in_date="2025-03-15",
            check_out_date="2025-03-20",
            num_guests=1,
        )

        if not results:
            logger.warning("No hotels found for the request")
            return {
                "errors": ["No hotels available at the destination"],
                "messages": [AIMessage(content="No hotels found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        hotel_booking = HotelBooking(**booking_data)

        logger.info(
            "Hotel booked: %s - %s at $%.2f/night",
            hotel_booking.hotel_name,
            hotel_booking.room_type,
            hotel_booking.price_per_night,
        )

        return {
            "hotel_bookings": [hotel_booking],
            "messages": [
                AIMessage(
                    content=f"Hotel booked: {hotel_booking.hotel_name} "
                    f"({hotel_booking.room_type}) "
                    f"at ${hotel_booking.price_per_night:.2f}/night"
                )
            ],
        }

    except Exception as error:
        logger.error("Hotel booking failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Hotel booking error: {str(error)}"],
            "messages": [AIMessage(content=f"Hotel booking failed: {str(error)}")],
        }
