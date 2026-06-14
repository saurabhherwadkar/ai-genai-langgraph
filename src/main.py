"""Main entry point for the Travel Booking Multi-Agent System.

This module provides the primary execution interface for running
the travel booking workflow graph with user requests.
"""

import sys  # System interface for exit codes

from src.graph import build_travel_graph  # Graph construction function
from src.utils.config_loader import load_settings  # Configuration loader
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the main module
logger = get_logger(__name__)


def run_travel_booking(user_request: str) -> str:
    """Execute the complete travel booking workflow for a user request.

    Builds the agent graph, initializes state with the user request,
    and runs the workflow to produce a consolidated booking summary.

    Args:
        user_request: Natural language description of the travel needs.

    Returns:
        Final booking summary string with all confirmed reservations.
    """
    # Log the start of a new booking workflow
    logger.info("Starting travel booking workflow")

    # Load application settings for configuration
    settings = load_settings()

    # Log the loaded environment for context
    logger.info(
        "Running in %s environment",
        settings.get("app", {}).get("environment", "unknown"),
    )

    # Build the compiled state graph
    graph = build_travel_graph()

    # Define the initial state for the workflow
    initial_state = {
        "user_request": user_request,
        "parsed_request": {},
        "required_services": [],
        "flight_bookings": [],
        "hotel_bookings": [],
        "car_rental_bookings": [],
        "bus_bookings": [],
        "train_bookings": [],
        "tour_package_bookings": [],
        "sightseeing_bookings": [],
        "errors": [],
        "final_summary": "",
        "messages": [],
    }

    # Execute the graph with the initial state
    logger.info("Invoking graph with user request")
    final_state = graph.invoke(initial_state)

    # Extract the final summary from the completed state
    summary = final_state.get("final_summary", "No summary generated.")

    # Log workflow completion
    logger.info("Travel booking workflow completed successfully")

    # Return the consolidated summary to the caller
    return summary


def main() -> None:
    """Main function demonstrating the multi-agent travel booking system.

    Runs a sample travel request through the workflow and prints
    the resulting booking summary.
    """
    # Define a sample travel request for demonstration
    sample_request = (
        "I need to book a flight from New York to London, "
        "find a hotel for 5 nights, rent a car for local travel, "
        "and arrange some sightseeing activities and a city tour package."
    )

    # Print the user request for visibility
    print("\n[User Request]")
    print(f"   {sample_request}\n")

    try:
        # Execute the travel booking workflow
        result = run_travel_booking(sample_request)

        # Print the final booking summary
        print("\n" + result)

    except Exception as error:
        # Log and display any unhandled errors
        logger.critical("Workflow failed: %s", str(error), exc_info=True)
        print(f"\n[ERROR] {str(error)}")
        sys.exit(1)


# Entry point guard for direct script execution
if __name__ == "__main__":
    main()
