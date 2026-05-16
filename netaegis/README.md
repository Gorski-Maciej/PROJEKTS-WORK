# NetAegis

Kompletny kod projektu wygenerowany na podstawie `_yy.txt`.

## Co zawiera projekt
- Main MCP (FastAPI): auth, dashboard, incidents, sync, actions, policies, recommendations, predictions, realtime health, websocket live.
- Operational MCP (FastAPI): agents, sync, actions execute, status i buffer.
- Agenci: netpulse, seclog (parsery auth/nginx), netconfig (Jinja2 templates).
- Frontend: React + Vite (Dashboard, Incidents, Recommendations + live websocket hook).
- Infra: Dockerfiles, docker-compose, Kubernetes manifests, Pulumi examples, CI.

## Uruchomienie lokalne
```bash
cd netaegis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server.main_mcp.app:app --port 8000 --reload
uvicorn server.operational_mcp.app:app --port 8001 --reload
```

## Uruchomienie przez kontenery
```bash
cd netaegis
docker compose up --build
```

## Testy
```bash
pytest -q netaegis/tests/test_mcp_flow.py
```
