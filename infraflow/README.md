# InfraFlow

InfraFlow to zaawansowany system self-healing do automatyzacji operacji infrastrukturalnych: monitoring przez SSH, reguły warunkowe, akcje naprawcze, harmonogram, API, dashboard i observability.

## Funkcje
- Asynchroniczne checki: CPU / RAM / disk / service.
- Rule engine oparty o AST (bezpieczna ewaluacja warunków).
- Akcje naprawcze: restart serwisów, czyszczenie logów, Ansible playbook, webhook/Slack/email.
- API FastAPI: JWT token, lista serwerów, uruchamianie checków manualnie, incydenty, websocket.
- Monitoring: Prometheus + Grafana.
- Persistence: TimescaleDB/PostgreSQL + Redis.

## Szybki start
```bash
cp .env.example .env
docker compose up --build
```

## Endpointy
- API docs: http://localhost:8000/docs
- GET `/health`
- POST `/token`
- GET `/servers`
- GET `/servers/{server_name}/status`
- POST `/servers/{server_name}/run-checks`
- GET `/incidents`
- GET `/metrics`
- PUT `/config/servers` (admin, zapis + commit `engine/config/servers.yml`)

## UI i obserwowalność
- Dashboard: http://localhost:8080
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

- GET `/queue-depth`

Scheduler odkłada zadania do Redis (`infraflow:jobs`), a dedykowany worker je konsumuje i wykonuje checki/akcje.

WebSocket (`/ws`) streamuje zdarzenia z kanału Redis `server_updates`.


## Lista kontrolna przed uruchomieniem
1. Wygeneruj klucz SSH dla przykładowej konfiguracji: `bash scripts/setup_keys.sh`.
2. Zmień hosty w `engine/config/servers.yml` na rzeczywiste serwery.
3. Sprawdź połączenie do TimescaleDB/Redis przez `docker compose up --build`.

Grafana dashboard jest dostępny w repo: `grafana/dashboards/infraflow-dashboard.json`.
