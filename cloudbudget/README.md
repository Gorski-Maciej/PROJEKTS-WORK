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


## Required bootstrap files
- Copy `.env.example` to `.env` and fill secrets for your providers and Keycloak.
- Initialize local OLAP schema:
  ```bash
  python scripts/init_duckdb.py
  ```

## Docker stack
```bash
cd cloudbudget
docker compose up -d --build
```


## Included production scaffolding
- `analytics/dbt_models/cost_daily_agg.sql` – dbt model for daily cost aggregation.
- `auth/keycloak/realm-export.json` – starter Keycloak realm/client/roles export.
- `monitoring/grafana/dashboards/cloudbudget-overview.json` – baseline Grafana dashboard for API traffic/latency.
- `.github/workflows/cloudbudget-ci.yml` – CI workflow (install + pytest).

## Main endpoints
- `GET /api/v1/healthz`
- `POST /api/v1/costs/ingest`
- `GET /api/v1/costs/summary/{tenant_id}`
- `POST /api/v1/recommendations/generate/{tenant_id}`
- `POST /api/v1/budgets`
- `GET /api/v1/budgets/{tenant_id}`
- `GET /api/v1/predictions/{tenant_id}`
- `POST /api/v1/simulations/what-if`
- `POST /api/v1/whatif/architecture-migration`
- `GET /api/v1/multicloud/providers`
- `POST /api/v1/multicloud/collect`
- `WS /ws/costs`


## Pulumi stack shape
- `infrastructure/pulumi/__main__.py` exports deployment knobs (replicas/storage/region) and checks secret presence from Pulumi config.
- Configure with `pulumi config set` / `pulumi config set --secret` before `pulumi up`.
