"""LangGraph workflow definition for the travel booking multi-agent system.

This module defines the state graph that orchestrates multiple specialized
booking agents. The orchestrator agent analyzes requests and routes them
to the appropriate service agents using conditional branching.
"""

from typing import Any  # Generic type annotations

from langgraph.graph import END, START, StateGraph  # Core graph components

from src.agents.bus_agent import bus_agent_node  # Bus booking node
from src.agents.car_rental_agent import car_rental_agent_node  # Car rental node
from src.agents.flight_agent import flight_agent_node  # Flight booking node
from src.agents.hotel_agent import hotel_agent_node  # Hotel booking node
from src.agents.orchestrator_agent import orchestrator_node  # Router node
from src.agents.sightseeing_agent import sightseeing_agent_node  # Activity node
from src.agents.summary_agent import summary_agent_node  # Summary node
from src.agents.tour_agent import tour_agent_node  # Tour package node
from src.agents.train_agent import train_agent_node  # Train booking node
from src.models.travel_state import TravelState  # Shared state schema
from src.utils.logger import get_logger  # Application logger

# Initialize module-level logger for the graph module
logger = get_logger(__name__)

# Map service names to their corresponding node identifiers
SERVICE_NODE_MAP: dict[str, str] = {
    "flight": "flight_agent",
    "hotel": "hotel_agent",
    "car_rental": "car_rental_agent",
    "bus": "bus_agent",
    "train": "train_agent",
    "tour_package": "tour_agent",
    "sightseeing": "sightseeing_agent",
}


def _route_to_agents(state: TravelState) -> list[str]:
    """Conditional routing function that determines which agents to invoke.

    Examines the required_services field in state and returns the list
    of agent nodes that should execute in parallel.

    Args:
        state: Current graph state with required services identified.

    Returns:
        List of node names to invoke next.
    """
    # Extract the list of required services from state
    required = state.get("required_services", [])

    # Map each required service to its corresponding graph node
    nodes_to_invoke = []
    for service in required:
        # Look up the node name for this service type
        node_name = SERVICE_NODE_MAP.get(service)
        if node_name:
            nodes_to_invoke.append(node_name)
            logger.debug("Routing to node: %s", node_name)

    # Fallback to summary if no valid services were identified
    if not nodes_to_invoke:
        logger.warning("No valid services to route to, going to summary")
        return ["summary_agent"]

    # Log the complete routing decision
    logger.info("Routing to %d agent(s): %s", len(nodes_to_invoke), nodes_to_invoke)

    # Return the list of nodes for parallel execution
    return nodes_to_invoke


def build_travel_graph() -> StateGraph:
    """Construct the complete travel booking state graph.

    Creates a LangGraph StateGraph with all agent nodes connected
    through conditional routing from the orchestrator.

    Returns:
        Compiled StateGraph ready for execution.
    """
    # Log the start of graph construction
    logger.info("Building travel booking graph")

    # Initialize the state graph with the TravelState schema
    graph = StateGraph(TravelState)

    # Add the orchestrator node as the entry point
    graph.add_node("orchestrator", orchestrator_node)

    # Add all specialized booking agent nodes
    graph.add_node("flight_agent", flight_agent_node)
    graph.add_node("hotel_agent", hotel_agent_node)
    graph.add_node("car_rental_agent", car_rental_agent_node)
    graph.add_node("bus_agent", bus_agent_node)
    graph.add_node("train_agent", train_agent_node)
    graph.add_node("tour_agent", tour_agent_node)
    graph.add_node("sightseeing_agent", sightseeing_agent_node)

    # Add the summary aggregation node
    graph.add_node("summary_agent", summary_agent_node)

    # Connect the graph start to the orchestrator
    graph.add_edge(START, "orchestrator")

    # Add conditional branching from orchestrator to service agents
    graph.add_conditional_edges(
        source="orchestrator",
        path=_route_to_agents,
        path_map={
            "flight_agent": "flight_agent",
            "hotel_agent": "hotel_agent",
            "car_rental_agent": "car_rental_agent",
            "bus_agent": "bus_agent",
            "train_agent": "train_agent",
            "tour_agent": "tour_agent",
            "sightseeing_agent": "sightseeing_agent",
            "summary_agent": "summary_agent",
        },
    )

    # Connect all service agent nodes to the summary node
    graph.add_edge("flight_agent", "summary_agent")
    graph.add_edge("hotel_agent", "summary_agent")
    graph.add_edge("car_rental_agent", "summary_agent")
    graph.add_edge("bus_agent", "summary_agent")
    graph.add_edge("train_agent", "summary_agent")
    graph.add_edge("tour_agent", "summary_agent")
    graph.add_edge("sightseeing_agent", "summary_agent")

    # Connect the summary node to the graph end
    graph.add_edge("summary_agent", END)

    # Compile the graph into an executable workflow
    compiled_graph = graph.compile()

    # Log successful graph compilation
    logger.info("Travel booking graph compiled successfully")

    # Return the compiled and ready-to-execute graph
    return compiled_graph
