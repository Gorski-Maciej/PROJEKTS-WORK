# CloudBudget 2.0 scope implemented

This repository includes implementation for:
- Multi-cloud ingestion with normalized records and API-triggered collection (`/api/v1/multicloud/*`).
- FinOps API for costs, budgets, predictions, recommendations, simulations, exports and reconciliation.
- Alert evaluation endpoint and invoice parsing/reconciliation endpoints.
- Action execution audit model/service and autopilot orchestration primitives.
- Realtime websocket heartbeat stream.
- Celery queues and scheduler helper.
- Docker stack, CI workflow, monitoring rules/dashboard, and Helm/Pulumi deployment scaffolding.
