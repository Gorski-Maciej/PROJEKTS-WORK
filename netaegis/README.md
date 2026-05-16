# NetAegis

Kompletny kod projektu wygenerowany na podstawie `_yy.txt`.

## Co zawiera projekt
- Main MCP (FastAPI): auth, dashboard, incidents, sync, actions, policies, recommendations, predictions, realtime health, websocket live.
- Operational MCP (FastAPI): agents, sync, actions execute, status i buffer.
- Agenci: netpulse, seclog (parsery auth/nginx), netconfig (Jinja2 templates, SSH collect/push, lokalne backupy Git).
- Frontend: React + Vite (Dashboard, Incidents, Recommendations + live websocket hook).
- Infra: Dockerfiles, docker-compose, Kubernetes manifests, Pulumi examples, CI.

## Uruchomienie lokalne (bez kontenerów)
```bash
cd netaegis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn server.main_mcp.app:app --port 8000 --reload
uvicorn server.operational_mcp.app:app --port 8001 --reload
```

## Uruchomienie przez kontenery (pełny stack z agentami)
```bash
cd netaegis
cp .env.example .env
# opcjonalnie: dostosuj wartości w .env do swojego środowiska

docker compose --env-file .env up --build
```

## Konfiguracja agentów
Agenci są konfigurowani przez zmienne środowiskowe:
- `netpulse`: `NETPULSE_AGENT_ID`, `NETPULSE_INTERVAL`, `NETPULSE_GATEWAY_IP`, `NETPULSE_APP_HOST`, `NETPULSE_APP_PORT`
- `seclog`: `SECLOG_AGENT_ID`, `SECLOG_WATCH_PATHS`
- `netconfig`: `NETCONFIG_AGENT_ID`, `NETCONFIG_LOCAL_REPO`, `NETCONFIG_DEVICE_IP`, `NETCONFIG_DEVICE_USERNAME`, `NETCONFIG_DEVICE_PASSWORD`

Przykładowa konfiguracja znajduje się w pliku `.env.example`.

## Testy
```bash
cd netaegis
pytest -q tests/test_mcp_flow.py tests/test_agents.py
```
