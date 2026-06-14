# Travel Booking Multi-Agent System

A multi-agent orchestration system built with **LangGraph 1.2.5** that demonstrates how to coordinate multiple specialized AI agents to handle complex travel booking workflows. Each agent has a single responsibility — booking flights, hotels, rental cars, buses, trains, tour packages, or local sightseeing activities.

---

## Table of Contents

- [About the Project](#about-the-project)
- [Architecture & Flow Diagram](#architecture--flow-diagram)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Deployment](#deployment)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Running Tests](#running-tests)
- [External Configuration](#external-configuration)
  - [Environment Variables](#environment-variables)
  - [Settings File](#settings-file)
  - [Log Level Configuration](#log-level-configuration)

---

## About the Project

This project demonstrates a production-grade multi-agent system where:

- An **Orchestrator Agent** analyzes user travel requests and determines which booking services are needed
- **Specialized Agents** (Flight, Hotel, Car Rental, Bus, Train, Tour, Sightseeing) execute independently and in parallel
- A **Summary Agent** consolidates all booking results into a unified itinerary
- **LangGraph's StateGraph** manages the workflow with conditional routing and parallel execution

### Key Design Principles

| Principle | Implementation |
|-----------|---------------|
| Single Responsibility | Each agent handles exactly one booking type |
| Separation of Concerns | Services, agents, models, and utilities are isolated packages |
| Security by Default | Input sanitization prevents injection attacks |
| Configurable | All environment-specific values live in `config/settings.yaml` |
| Observable | Structured logging with configurable levels |
| Testable | Comprehensive unit and integration tests |

---

## Architecture & Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER REQUEST                              │
│  "Book a flight, hotel, car rental, and sightseeing in London"  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   ORCHESTRATOR AGENT  │
              │  (Parse & Route)      │
              └───────────┬───────────┘
                          │
          ┌───────────────┼───────────────┐
          │ Conditional   │ Routing       │
          │ (parallel)    │               │
          ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ FLIGHT AGENT │ │ HOTEL AGENT  │ │ CAR RENTAL   │
│              │ │              │ │    AGENT     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       │    ┌───────────┼─────────┐       │
       │    │           │         │       │
       ▼    ▼           ▼         ▼       ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  BUS AGENT   │ │ TRAIN AGENT  │ │  TOUR AGENT  │
│              │ │              │ │              │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       │         ┌──────┴──────┐          │
       │         │             │          │
       ▼         ▼             ▼          ▼
       │  ┌──────────────┐              │
       │  │ SIGHTSEEING  │              │
       │  │    AGENT     │              │
       │  └──────┬───────┘              │
       │         │                      │
       └─────────┼──────────────────────┘
                 │
                 ▼
       ┌───────────────────┐
       │  SUMMARY AGENT    │
       │ (Consolidate All) │
       └─────────┬─────────┘
                 │
                 ▼
       ┌───────────────────┐
       │  BOOKING SUMMARY  │
       │   (Final Output)  │
       └───────────────────┘
```

**Workflow Steps:**

1. User submits a natural language travel request
2. Orchestrator parses the request and identifies required services
3. LangGraph routes to relevant agents via conditional edges (parallel execution)
4. Each specialized agent searches and books through its respective service
5. All results converge at the Summary Agent
6. A consolidated itinerary is returned to the user

---

## Project Structure

```
ai-genai-langgraph/
├── config/
│   ├── __init__.py              # Config package marker
│   └── settings.yaml            # Application configuration (env-specific)
├── src/
│   ├── __init__.py              # Source package marker
│   ├── main.py                  # Application entry point
│   ├── graph.py                 # LangGraph workflow definition
│   ├── agents/
│   │   ├── __init__.py          # Agents package exports
│   │   ├── orchestrator_agent.py # Request parsing and routing
│   │   ├── flight_agent.py      # Flight search and booking
│   │   ├── hotel_agent.py       # Hotel search and booking
│   │   ├── car_rental_agent.py  # Car rental operations
│   │   ├── bus_agent.py         # Bus booking operations
│   │   ├── train_agent.py       # Train booking operations
│   │   ├── tour_agent.py        # Tour package operations
│   │   ├── sightseeing_agent.py # Sightseeing activity booking
│   │   └── summary_agent.py     # Result consolidation
│   ├── models/
│   │   ├── __init__.py          # Models package exports
│   │   ├── travel_state.py      # LangGraph state definition
│   │   └── booking_schemas.py   # Pydantic data validation schemas
│   ├── services/
│   │   ├── __init__.py          # Services package exports
│   │   ├── base_service.py      # Abstract base service class
│   │   ├── flight_service.py    # Flight API integration
│   │   ├── hotel_service.py     # Hotel API integration
│   │   ├── car_rental_service.py # Car rental API integration
│   │   ├── bus_service.py       # Bus API integration
│   │   ├── train_service.py     # Train API integration
│   │   ├── tour_service.py      # Tour package API integration
│   │   └── sightseeing_service.py # Sightseeing API integration
│   └── utils/
│       ├── __init__.py          # Utils package exports
│       ├── config_loader.py     # YAML configuration reader
│       ├── logger.py            # Centralized logging setup
│       └── input_sanitizer.py   # Input validation and security
├── tests/
│   ├── __init__.py              # Test package marker
│   ├── test_config_loader.py    # Configuration loader tests
│   ├── test_input_sanitizer.py  # Input sanitization tests
│   ├── test_services.py         # Booking service tests
│   ├── test_orchestrator.py     # Orchestrator agent tests
│   ├── test_booking_schemas.py  # Schema validation tests
│   └── test_graph.py            # End-to-end graph integration tests
├── logs/                        # Generated log files (gitignored)
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore patterns
├── pyproject.toml               # Build and tool configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langgraph | 1.2.5 | Multi-agent workflow orchestration |
| langchain-core | 0.3.63 | Foundation for LangChain components |
| langchain-openai | 0.3.18 | OpenAI LLM integration |
| pydantic | 2.11.3 | Data validation and schema enforcement |
| pyyaml | 6.0.2 | YAML configuration file parsing |
| httpx | 0.28.1 | HTTP client for API calls |
| pytest | 8.4.0 | Test framework |
| ruff | 0.11.12 | Linting and formatting |

---

## Deployment

### Prerequisites

- **Python 3.11+** (required for modern type hints)
- **pip** package manager
- **Git** for version control

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd ai-genai-langgraph
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Running the Application

```bash
# Run the demo travel booking workflow
python -m src.main
```

**Expected output:**

```
User Request:
   I need to book a flight from New York to London, find a hotel...

==================================================
  TRAVEL BOOKING SUMMARY
==================================================

--- FLIGHTS ---
  SkyWings Airlines SW-201: New York -> London
  Departure: 2025-03-15T08:00:00 | Price: $450.00
  Booking ID: FLT-a1b2c3d4

--- HOTELS ---
  Grand Plaza Hotel (Deluxe Double)
  Check-in: 2025-03-15 | Check-out: 2025-03-20
  Rate: $180.00/night | ID: HTL-e5f6g7h8
...
```

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/test_graph.py -v

# Run with debug logging
LOG_LEVEL=DEBUG pytest -v
```

---

## External Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes* | — | OpenAI API key (*required only for LLM-powered features) |
| `LOG_LEVEL` | No | `INFO` | Application log level |
| `CONFIG_PATH` | No | `config/settings.yaml` | Custom config file path |

### Settings File

All configurable values are in `config/settings.yaml`. Key sections:

- **`app`** — Application name, version, environment
- **`logging`** — Log level, format, file rotation settings
- **`llm`** — Model provider, model name, temperature, timeouts
- **`agents`** — Max iterations, recursion limits
- **`services`** — Base URLs and timeouts for each booking API
- **`rate_limiting`** — Request throttling configuration
- **`security`** — Input validation limits

### Log Level Configuration

Set via `LOG_LEVEL` environment variable or in `config/settings.yaml`:

```yaml
logging:
  level: "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

Log files are written to `logs/travel_agent.log` with automatic rotation at 10 MB.
