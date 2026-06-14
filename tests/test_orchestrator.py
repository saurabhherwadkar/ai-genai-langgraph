"""Unit tests for the orchestrator agent module."""

import pytest  # Test framework

from src.agents.orchestrator_agent import OrchestratorAgent, orchestrator_node


class TestOrchestratorAgent:
    """Test suite for the OrchestratorAgent class."""

    def setup_method(self) -> None:
        """Set up a fresh agent instance for each test."""
        self.agent = OrchestratorAgent()

    def test_identifies_flight_service(self) -> None:
        """Verify flight keywords are detected in user request."""
        state = {
            "user_request": "I need to fly from NYC to London",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "flight" in result["required_services"]

    def test_identifies_hotel_service(self) -> None:
        """Verify hotel keywords are detected in user request."""
        state = {
            "user_request": "Book a hotel in Paris for 3 nights",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "hotel" in result["required_services"]

    def test_identifies_multiple_services(self) -> None:
        """Verify multiple service types are detected together."""
        state = {
            "user_request": "I need a flight, hotel, and car rental in London",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        services = result["required_services"]
        assert "flight" in services
        assert "hotel" in services
        assert "car_rental" in services

    def test_identifies_train_service(self) -> None:
        """Verify train keywords are detected in user request."""
        state = {
            "user_request": "Book a train from London to Paris",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "train" in result["required_services"]

    def test_identifies_bus_service(self) -> None:
        """Verify bus keywords are detected in user request."""
        state = {
            "user_request": "I want to take a bus to Boston",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "bus" in result["required_services"]

    def test_identifies_tour_package(self) -> None:
        """Verify tour package keywords are detected."""
        state = {
            "user_request": "Find me a guided tour package in Rome",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "tour_package" in result["required_services"]

    def test_identifies_sightseeing(self) -> None:
        """Verify sightseeing keywords are detected."""
        state = {
            "user_request": "I want to explore museums and attractions",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "sightseeing" in result["required_services"]

    def test_defaults_to_flight_and_hotel(self) -> None:
        """Verify default services when no keywords match."""
        state = {
            "user_request": "I want to go somewhere nice",
            "messages": [],
        }
        result = self.agent.parse_request(state)
        assert "flight" in result["required_services"]
        assert "hotel" in result["required_services"]

    def test_orchestrator_node_function(self) -> None:
        """Verify the node function wrapper works correctly."""
        state = {
            "user_request": "Book a flight to Tokyo",
            "messages": [],
        }
        result = orchestrator_node(state)
        assert "required_services" in result
        assert "flight" in result["required_services"]
