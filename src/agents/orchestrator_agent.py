"""Orchestrator agent responsible for routing travel requests to specialized agents.

This module contains the primary routing logic that analyzes user requests
and determines which specialized booking agents should be invoked.
"""

import json  # JSON serialization for structured data
from typing import Any  # Generic type annotations

from langchain_core.messages import HumanMessage  # Message type for user input

from src.models.travel_state import TravelState  # Graph state definition
from src.utils.input_sanitizer import sanitize_string  # Input security
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the orchestrator
logger = get_logger(__name__)

# Mapping of keywords to service types for request classification
SERVICE_KEYWORDS: dict[str, list[str]] = {
    "flight": ["flight", "fly", "plane", "airline", "airport"],
    "hotel": ["hotel", "accommodation", "stay", "room", "lodge"],
    "car_rental": ["car", "rental", "vehicle", "drive", "automobile"],
    "bus": ["bus", "coach", "shuttle"],
    "train": ["train", "rail", "railway"],
    "tour_package": ["tour", "package", "guided", "excursion"],
    "sightseeing": ["sightseeing", "attraction", "museum", "activity", "explore"],
}


class OrchestratorAgent:
    """Agent responsible for parsing requests and routing to sub-agents.

    Analyzes the user's travel request to determine which services
    are needed and extracts structured booking parameters.
    """

    def __init__(self) -> None:
        """Initialize the orchestrator agent."""
        # Log initialization of the orchestrator
        logger.info("OrchestratorAgent initialized")

    def parse_request(self, state: TravelState) -> dict[str, Any]:
        """Parse the user request and determine required services.

        Analyzes the raw user request text to extract destinations,
        dates, and required service types for routing.

        Args:
            state: Current graph state containing the user request.

        Returns:
            State update dictionary with parsed request and services.
        """
        # Extract the raw user request from the state
        user_request = state.get("user_request", "")

        # Sanitize the input to prevent injection attacks
        safe_request = sanitize_string(user_request)

        # Log the incoming request for tracing
        logger.info("Parsing travel request: %s", safe_request[:100])

        # Determine which services are required based on keywords
        required_services = self._identify_services(safe_request)

        # If no specific services detected, default to common travel set
        if not required_services:
            logger.info("No specific services detected, using defaults")
            required_services = ["flight", "hotel"]

        # Build the parsed request structure with extracted details
        parsed_request = {
            "raw_query": safe_request,
            "required_services": required_services,
        }

        # Log the routing decision for debugging
        logger.info("Routing to services: %s", required_services)

        # Return the state update with parsed information
        return {
            "parsed_request": parsed_request,
            "required_services": required_services,
            "messages": [
                HumanMessage(
                    content=f"Processing travel request for services: "
                    f"{', '.join(required_services)}"
                )
            ],
        }

    def _identify_services(self, request_text: str) -> list[str]:
        """Identify required travel services from the request text.

        Scans the request text for keywords that indicate which
        booking services the user needs.

        Args:
            request_text: The sanitized user request text.

        Returns:
            List of identified service type strings.
        """
        # Convert request to lowercase for case-insensitive matching
        lower_request = request_text.lower()

        # Collect services whose keywords appear in the request
        identified = []
        for service, keywords in SERVICE_KEYWORDS.items():
            # Check if any keyword for this service appears in request
            if any(keyword in lower_request for keyword in keywords):
                identified.append(service)
                logger.debug("Identified service: %s", service)

        # Return the list of identified services
        return identified


def orchestrator_node(state: TravelState) -> dict[str, Any]:
    """LangGraph node function for the orchestrator agent.

    This function serves as the entry point for the orchestrator
    in the LangGraph workflow graph.

    Args:
        state: Current graph state.

    Returns:
        Updated state dictionary with routing information.
    """
    # Create orchestrator instance and delegate to parse method
    orchestrator = OrchestratorAgent()

    # Execute the parsing and routing logic
    return orchestrator.parse_request(state)
