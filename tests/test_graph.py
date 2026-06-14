"""Integration tests for the LangGraph travel booking workflow."""

import pytest  # Test framework

from src.graph import build_travel_graph, _route_to_agents  # Graph under test


class TestRouteToAgents:
    """Test suite for the routing function."""

    def test_routes_to_flight_agent(self) -> None:
        """Verify routing to flight agent for flight service."""
        state = {"required_services": ["flight"]}
        result = _route_to_agents(state)
        assert "flight_agent" in result

    def test_routes_to_multiple_agents(self) -> None:
        """Verify routing to multiple agents simultaneously."""
        state = {"required_services": ["flight", "hotel", "car_rental"]}
        result = _route_to_agents(state)
        assert "flight_agent" in result
        assert "hotel_agent" in result
        assert "car_rental_agent" in result

    def test_routes_to_summary_when_empty(self) -> None:
        """Verify fallback to summary when no services identified."""
        state = {"required_services": []}
        result = _route_to_agents(state)
        assert "summary_agent" in result

    def test_routes_all_service_types(self) -> None:
        """Verify all seven service types can be routed."""
        all_services = [
            "flight", "hotel", "car_rental", "bus",
            "train", "tour_package", "sightseeing",
        ]
        state = {"required_services": all_services}
        result = _route_to_agents(state)
        assert len(result) == 7


class TestBuildTravelGraph:
    """Test suite for graph construction."""

    def test_graph_compiles_successfully(self) -> None:
        """Verify the graph can be built and compiled without errors."""
        graph = build_travel_graph()
        assert graph is not None

    def test_graph_executes_flight_request(self) -> None:
        """Verify the graph executes a flight-only request end-to-end."""
        graph = build_travel_graph()
        initial_state = {
            "user_request": "I need a flight to London",
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
        result = graph.invoke(initial_state)
        assert result["final_summary"] != ""
        assert len(result["flight_bookings"]) > 0

    def test_graph_executes_multi_service_request(self) -> None:
        """Verify the graph handles multiple service types."""
        graph = build_travel_graph()
        initial_state = {
            "user_request": "Book a flight and hotel in London with sightseeing",
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
        result = graph.invoke(initial_state)
        assert len(result["flight_bookings"]) > 0
        assert len(result["hotel_bookings"]) > 0
        assert len(result["sightseeing_bookings"]) > 0
        assert "FLIGHTS" in result["final_summary"]
        assert "HOTELS" in result["final_summary"]

    def test_graph_produces_summary(self) -> None:
        """Verify the graph always produces a final summary."""
        graph = build_travel_graph()
        initial_state = {
            "user_request": "go somewhere",
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
        result = graph.invoke(initial_state)
        assert "TRAVEL BOOKING SUMMARY" in result["final_summary"]
