"""Tour package agent responsible for searching and booking tour packages.

This agent handles all tour package operations within the workflow.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import TourPackageBooking  # Tour schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.tour_service import TourService  # External tour API
from src.utils.logger import get_logger  # Application logger

logger = get_logger(__name__)


def tour_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books tour packages.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with tour package booking results.
    """
    logger.info("Tour agent processing request")

    service = TourService()

    try:
        results = service.search(
            destination="London",
            departure_date="2025-03-16",
            duration_days=3,
        )

        if not results:
            return {
                "errors": ["No tour packages available"],
                "messages": [AIMessage(content="No tours found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        tour_booking = TourPackageBooking(**booking_data)

        logger.info("Tour booked: %s by %s", tour_booking.package_name, tour_booking.operator)

        return {
            "tour_package_bookings": [tour_booking],
            "messages": [
                AIMessage(
                    content=f"Tour booked: {tour_booking.package_name} "
                    f"by {tour_booking.operator} "
                    f"at ${tour_booking.price_per_person:.2f}/person"
                )
            ],
        }

    except Exception as error:
        logger.error("Tour booking failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Tour booking error: {str(error)}"],
            "messages": [AIMessage(content=f"Tour booking failed: {str(error)}")],
        }
