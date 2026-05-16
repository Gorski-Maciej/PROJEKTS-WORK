# CloudBudget 2.0

CloudBudget 2.0 is a self-hosted, multi-tenant FinOps platform implementing:
- multi-cloud ingestion agents (AWS/Azure/GCP/On-Prem/Kubernetes),
- FastAPI backend with REST + WebSocket,
- asynchronous task execution using Celery + RabbitMQ,
- OLTP (PostgreSQL) and OLAP (DuckDB + Polars),
- budget monitoring, recommendations, and forecasting.

## Implemented modules
- **API routers:** health, costs ingest/summary, recommendations, simulations, budgets, predictions.
- **Realtime:** WebSocket endpoint `/ws/costs`.
- **Services:** ingestion, analytics, recommendation, simulation, budget, prediction, queue tasks.
- **Agents:** normalized cost records from providers.
- **Frontend:** Next.js dashboard consuming API endpoints.

## Quick start (local)
```bash
cd cloudbudget
python -m venv .venv && source .venv/bin/activate
pip install -e .
uvicorn api.main:app --reload --port 8000
```

## Docker stack
```bash
cd cloudbudget
docker compose up -d --build
```

## Main endpoints
- `GET /api/v1/healthz`
- `POST /api/v1/costs/ingest`
- `GET /api/v1/costs/summary/{tenant_id}`
- `POST /api/v1/recommendations/generate/{tenant_id}`
- `POST /api/v1/budgets`
- `GET /api/v1/budgets/{tenant_id}`
- `GET /api/v1/predictions/{tenant_id}`
- `POST /api/v1/simulations/what-if`
- `WS /ws/costs`
