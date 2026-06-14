"""Sightseeing agent responsible for booking local activities and attractions.

This agent handles all sightseeing-related operations within the workflow.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import SightseeingBooking  # Sightseeing schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.sightseeing_service import SightseeingService  # External API
from src.utils.logger import get_logger  # Application logger

logger = get_logger(__name__)


def sightseeing_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books sightseeing activities.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with sightseeing booking results.
    """
    logger.info("Sightseeing agent processing request")

    service = SightseeingService()

    try:
        results = service.search(
            location="London",
            date="2025-03-16",
        )

        if not results:
            return {
                "errors": ["No sightseeing activities available"],
                "messages": [AIMessage(content="No activities found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        sightseeing_booking = SightseeingBooking(**booking_data)

        logger.info("Activity booked: %s", sightseeing_booking.activity_name)

        return {
            "sightseeing_bookings": [sightseeing_booking],
            "messages": [
                AIMessage(
                    content=f"Activity booked: {sightseeing_booking.activity_name} "
                    f"by {sightseeing_booking.provider} "
                    f"at ${sightseeing_booking.price_per_person:.2f}/person"
                )
            ],
        }

    except Exception as error:
        logger.error("Sightseeing failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Sightseeing error: {str(error)}"],
            "messages": [AIMessage(content=f"Sightseeing failed: {str(error)}")],
        }
