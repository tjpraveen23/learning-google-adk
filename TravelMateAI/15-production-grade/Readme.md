# TravelMate AI – Production-Grade Multi-Agent Application

TravelMate AI is a **production-grade multi-agent travel planning application** built using **Google ADK (Agent Development Kit)**. The application demonstrates enterprise AI engineering patterns including **multi-agent orchestration, persistent memory, SQLite caching, streaming responses, structured logging, callbacks, Phoenix tracing, Docker, and GitHub Actions CI**.

This project was built as a capstone implementation after a structured ADK learning journey and is designed to showcase **production-ready AI application architecture**.

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
- Phoenix OpenTelemetry Tracing
- Docker Compose
```

## Features

### Multi-agent architecture

* **WeatherAgent** – Weather recommendations
* **HotelAgent** – Hotel suggestions
* **BudgetAgent** – Budget estimation
* **TravelCoordinator** – Final itinerary generation

### Persistent SQLite memory

* Conversation memory using **Google ADK DatabaseSessionService**
* Session continuity across application restarts
* Multiple user sessions

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
* Phoenix tracing
* OpenTelemetry integration

### Production-ready deployment

* Dockerized backend and frontend
* Docker Compose orchestration
* GitHub Actions CI pipeline
* Environment-based configuration
* Health-check validation

## Project structure

```text
TravelMateAI/
└── 15-production-grade/
    ├── app.py
    ├── streamlit_app.py
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    ├── backend/
    │   ├── .env.example
    │   ├── data/
    │   ├── logs/
    │   └── travel_agent/
    │       ├── config.py
    │       ├── database.py
    │       ├── cache.py
    │       ├── tracing.py
    │       ├── callbacks.py
    │       ├── orchestrator.py
    │       ├── coordinator.py
    │       ├── weather_agent.py
    │       ├── hotel_agent.py
    │       ├── budget_agent.py
    │       └── tools.py
    ├── frontend/
    └── testcases/
```

## Local installation

### Clone the repository

```bash
git clone https://github.com/tjpraveen23/learning-google-adk.git
cd learning-google-adk/TravelMateAI/15-production-grade
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

Create `backend/.env`.

```text
APP_NAME=travelmate
ENVIRONMENT=dev

MODEL_NAME=groq/llama-3.3-70b-versatile
GROQ_API_KEY=your_groq_api_key

SESSION_DB=data/sessions.db
CACHE_DB=data/cache.db

TRACING_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

WEATHER_CACHE_TTL=3600
HOTEL_CACHE_TTL=3600
BUDGET_CACHE_TTL=3600
```

## Running the application

### FastAPI

```bash
uvicorn app:app --reload
```

Backend

```text
http://127.0.0.1:8000
```

### Streamlit

```bash
python -m streamlit run streamlit_app.py
```

Frontend

```text
http://localhost:8501
```

## Running with Docker

Build and start the complete application.

```bash
docker compose up --build
```

Services

| Service   | URL                   |
| --------- | --------------------- |
| FastAPI   | http://localhost:8000 |
| Streamlit | http://localhost:8501 |
| Phoenix   | http://localhost:6006 |

Stop all services.

```bash
docker compose down
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

```bash
python testcases/test_config.py
python testcases/test_database.py
python testcases/test_cache.py
python testcases/test_tools.py
python testcases/test_agents.py
python testcases/test_stream.py
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

Logs are written to:

```text
backend/logs/travelmate.log
```

Sample log

```text
2026-08-02 20:15:31 | INFO | callbacks | request-id | Agent started
2026-08-02 20:15:36 | INFO | callbacks | request-id | Tool completed: get_weather in 5.01 sec
2026-08-02 20:15:37 | INFO | cache | request-id | Cache HIT: weather:chennai
```

## Tracing

Phoenix captures request spans, agent spans, and tool spans.

Open:

```text
http://localhost:6006
```

This provides end-to-end execution visibility for the complete agent workflow.

## CI pipeline

The project includes a **GitHub Actions CI pipeline** located at:

```text
.github/workflows/TravelMateAI-ci.yml
```

The pipeline automatically:

* Builds Docker images
* Starts backend and frontend containers
* Performs health checks
* Validates the FastAPI endpoint
* Cleans up containers

This ensures every change is validated automatically.

## Performance summary

Each request includes execution timing.

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

* Google ADK
* FastAPI
* Streamlit
* SQLite
* Phoenix
* OpenTelemetry
* Docker
* Docker Compose
* GitHub Actions
* Python
* AsyncIO
* Server-Sent Events (SSE)

## Production engineering concepts demonstrated

* Multi-agent orchestration
* Agent communication
* Streaming AI responses
* Persistent conversational memory
* Cache-aside pattern
* TTL-based caching
* Structured logging
* Distributed tracing
* Docker containerization
* CI automation
* Health checks
* Environment-based configuration
* Async Python architecture

## License

This project is intended for learning, portfolio, and demonstration purposes.
