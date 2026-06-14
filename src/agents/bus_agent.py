"""Bus booking agent responsible for searching and booking bus travel.

This agent handles all bus-related operations within the workflow.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import BusBooking  # Bus schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.bus_service import BusService  # External bus API
from src.utils.logger import get_logger  # Application logger

logger = get_logger(__name__)


def bus_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books bus tickets.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with bus booking results.
    """
    logger.info("Bus agent processing request")

    service = BusService()

    try:
        results = service.search(
            origin="New York",
            destination="Boston",
            departure_date="2025-03-15",
        )

        if not results:
            return {
                "errors": ["No bus routes available"],
                "messages": [AIMessage(content="No bus routes found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        bus_booking = BusBooking(**booking_data)

        logger.info("Bus booked: %s route %s", bus_booking.operator, bus_booking.route)

        return {
            "bus_bookings": [bus_booking],
            "messages": [
                AIMessage(
                    content=f"Bus booked: {bus_booking.operator} "
                    f"({bus_booking.route}) at ${bus_booking.price:.2f}"
                )
            ],
        }

    except Exception as error:
        logger.error("Bus booking failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Bus booking error: {str(error)}"],
            "messages": [AIMessage(content=f"Bus booking failed: {str(error)}")],
        }
