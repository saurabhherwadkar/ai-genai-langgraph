"""Car rental agent responsible for searching and booking vehicles.

This agent handles all car rental operations within the workflow.
"""

from typing import Any  # Generic type annotations

from langchain_core.messages import AIMessage  # Message type for agent output

from src.models.booking_schemas import CarRentalBooking  # Car rental schema
from src.models.travel_state import TravelState  # Graph state definition
from src.services.car_rental_service import CarRentalService  # External API
from src.utils.logger import get_logger  # Application logger

logger = get_logger(__name__)


def car_rental_agent_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node that searches and books rental cars.

    Args:
        state: Current graph state with parsed travel request.

    Returns:
        State update with car rental booking results.
    """
    logger.info("Car rental agent processing request")

    service = CarRentalService()

    try:
        results = service.search(
            pickup_location="London",
            pickup_date="2025-03-15",
            dropoff_date="2025-03-20",
        )

        if not results:
            return {
                "errors": ["No rental cars available"],
                "messages": [AIMessage(content="No rental cars found.")],
            }

        selected = results[0]
        booking_data = service.book(**selected)
        car_booking = CarRentalBooking(**booking_data)

        logger.info("Car booked: %s from %s", car_booking.vehicle_type, car_booking.company)

        return {
            "car_rental_bookings": [car_booking],
            "messages": [
                AIMessage(
                    content=f"Car rental booked: {car_booking.vehicle_type} "
                    f"from {car_booking.company} at ${car_booking.daily_rate:.2f}/day"
                )
            ],
        }

    except Exception as error:
        logger.error("Car rental failed: %s", str(error), exc_info=True)
        return {
            "errors": [f"Car rental error: {str(error)}"],
            "messages": [AIMessage(content=f"Car rental failed: {str(error)}")],
        }
