# TravelMate AI – Production-Grade Multi-Agent Application

TravelMate AI is a **production-grade multi-agent travel planning application** built using **Google ADK (Agent Development Kit)**. The application demonstrates enterprise AI engineering patterns including **multi-agent orchestration, persistent memory, SQLite caching, streaming responses, structured logging, callbacks, tracing, FastAPI, and Streamlit**.

This project was built as a capstone implementation after a structured 15-day ADK learning journey and is designed to be **deployment-ready with Docker, GitHub Actions, and Harness CI/CD**.

## Architecture

```text
                 +----------------------+
                 |     Streamlit UI     |
                 |  Chat + History UI   |
                 +----------+-----------+
                            |
                            |
                 Streaming HTTP (SSE)
                            |
                            |
                 +----------v-----------+
                 |      FastAPI API     |
                 |  Streaming Endpoint  |
                 +----------+-----------+
                            |
                            |
                 +----------v-----------+
                 |     Orchestrator     |
                 |  Streaming Generator |
                 +-----+--------+-------+
                       |        |
             invokes   |        | invokes
                       |        |
          +------------v-+   +--v------------+
          | WeatherAgent |   | HotelAgent    |
          +--------------+   +---------------+
                       |
          +------------v--------------+
          | BudgetAgent               |
          +---------------------------+
                       |
          +------------v--------------+
          | TravelCoordinator         |
          +---------------------------+
                       |
          +------------v--------------+
          | Final Recommendation      |
          +---------------------------+

Supporting Services
- SQLite Session Memory
- SQLite Cache (TTL)
- Structured Logging
- ADK Callbacks
- OpenTelemetry Tracing
```

## Features

### Multi-agent architecture

* **WeatherAgent** – Weather recommendations
* **HotelAgent** – Hotel suggestions
* **BudgetAgent** – Budget estimation
* **TravelCoordinator** – Final itinerary generation

### Persistent SQLite memory

* Conversation memory stored using **Google ADK DatabaseSessionService**
* Session continuity across application restarts
* Separate user sessions supported

### SQLite caching

* TTL-based caching
* Weather cache
* Hotel cache
* Budget cache
* Automatic cache expiration
* Cache hit/miss logging

### Streaming responses

* Real-time agent execution updates
* FastAPI Server-Sent Events (SSE)
* Streamlit live progress display
* Incremental UI updates

### Observability

* Structured logging with request IDs
* Agent execution timing
* Tool execution timing
* ADK callbacks
* OpenTelemetry tracing foundation

### Production UI

* Chat interface
* Session history sidebar
* New session support
* Performance summary
* Real-time agent status

## Project structure

```text
15-production-grade/

├── app.py                     # FastAPI application
├── streamlit_app.py           # Streamlit UI
├── requirements.txt
├── .env
├── Dockerfile
│
├── data/
│   ├── travelmate.db          # ADK session memory
│   ├── cache.db               # SQLite cache
│   └── trace.db               # Trace storage
│
├── logs/
│   └── travelmate.log
│
├── travel_agent/
│   ├── __init__.py
│   ├── config.py
│   ├── logger.py
│   ├── database.py
│   ├── cache.py
│   ├── tracing.py
│   ├── callbacks.py
│   ├── orchestrator.py
│   ├── coordinator.py
│   ├── weather_agent.py
│   ├── hotel_agent.py
│   ├── budget_agent.py
│   └── tools.py
│
└── testcases/
    ├── test_config.py
    ├── test_database.py
    ├── test_cache.py
    ├── test_tools.py
    ├── test_agents.py
    ├── test_stream.py
    └── test_fastapi.py
```

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/travelmate-ai.git
cd travelmate-ai
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

Windows

```bash
.venv\\Scripts\\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Environment configuration

Create a `.env` file.

```text
APP_NAME=travelmate
ENVIRONMENT=dev

MODEL=groq/llama-3.3-70b-versatile

SESSION_DB=data/travelmate.db
CACHE_DB=data/cache.db
TRACE_DB=data/trace.db

WEATHER_CACHE_TTL=1800
HOTEL_CACHE_TTL=3600
BUDGET_CACHE_TTL=86400
ITINERARY_CACHE_TTL=900

FILE_LOG_ENTRY=yes
```

## Running the application

### Start FastAPI

```bash
uvicorn app:app --reload
```

API available at

```text
http://127.0.0.1:8000
```

### Start Streamlit

```bash
python -m streamlit run streamlit_app.py
```

UI available at

```text
http://localhost:8501
```

## API endpoints

### Health check

```http
GET /health
```

Response

```json
{
  "status": "healthy",
  "service": "travelmate"
}
```

### Streaming travel planning

```http
POST /travel
```

Request

```json
{
  "prompt": "Plan a Chennai trip under 20000",
  "user_id": "praveen_tj"
}
```

Response

Server-Sent Events (SSE)

```text
WeatherAgent started
WeatherAgent completed
HotelAgent started
HotelAgent completed
BudgetAgent started
BudgetAgent completed
TravelCoordinator running
Final recommendation
```

## Testing

Run individual components.

### Configuration

```bash
python testcases/test_config.py
```

### Database

```bash
python testcases/test_database.py
```

### Cache

```bash
python testcases/test_cache.py
```

### Tools

```bash
python testcases/test_tools.py
```

### Individual agents

```bash
python testcases/test_agents.py
```

### Streaming orchestrator

```bash
python testcases/test_stream.py
```

### FastAPI streaming

```bash
python testcases/test_fastapi.py
```

## Caching behavior

First request

```text
Cache MISS
Weather API call
Result stored
```

Subsequent request

```text
Cache HIT
Result returned immediately
```

This significantly reduces latency for repeated travel requests.

## Logging

Logs are written to

```text
logs/travelmate.log
```

Sample log

```text
2026-08-02 20:15:31 | INFO | callbacks | request-id | Agent started
2026-08-02 20:15:36 | INFO | callbacks | request-id | Tool completed: get_weather in 5.01 sec
2026-08-02 20:15:37 | INFO | cache | request-id | Cache HIT: weather:chennai
```

## Performance tracking

Each request includes a performance summary.

Example

```json
{
  "WeatherAgent": 5.01,
  "HotelAgent": 10.02,
  "BudgetAgent": 2.01,
  "TravelCoordinator": 0.35,
  "Total": 17.39
}
```

## Technology stack

* **Google ADK**
* **FastAPI**
* **Streamlit**
* **SQLite**
* **OpenTelemetry**
* **Python 3.14**
* **Server-Sent Events (SSE)**
* **Structured Logging**
* **AsyncIO**

## Production roadmap

Planned production enhancements.

* Docker containerization
* Docker Compose
* GitHub Actions CI
* Harness CD
* Secrets management
* Health checks
* Readiness probes
* Metrics and monitoring
* Horizontal scaling
* External cache (Redis)
* Cloud database support

## Learning outcomes

This project demonstrates practical implementation of:

* Multi-agent orchestration
* Agent communication
* Streaming AI responses
* Persistent conversational memory
* Caching strategies
* Observability
* Production logging
* Tracing
* Async Python
* FastAPI APIs
* Streamlit real-time interfaces
* Enterprise AI application architecture

## License

This project is intended for learning, portfolio, and demonstration purposes.
