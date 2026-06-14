"""Train booking agent responsible for searching and booking rail travel.

This agent handles all train-related operations within the workflow.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import TrainBooking  # Train schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.train_service import TrainService  # External train API
from src.utils.logger import get_logger  # Application logger

logger = get_logger(__name__)


def train_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books train tickets.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with train booking results.
    """
    logger.info("Train agent processing request")

    service = TrainService()

    try:
        results = service.search(
            origin="London",
            destination="Paris",
            departure_date="2025-03-16",
        )

        if not results:
            return {
                "errors": ["No train services available"],
                "messages": [AIMessage(content="No trains found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        train_booking = TrainBooking(**booking_data)

        logger.info("Train booked: %s %s", train_booking.operator, train_booking.train_number)

        return {
            "train_bookings": [train_booking],
            "messages": [
                AIMessage(
                    content=f"Train booked: {train_booking.operator} "
                    f"{train_booking.train_number} at ${train_booking.price:.2f}"
                )
            ],
        }

    except Exception as error:
        logger.error("Train booking failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Train booking error: {str(error)}"],
            "messages": [AIMessage(content=f"Train booking failed: {str(error)}")],
        }
