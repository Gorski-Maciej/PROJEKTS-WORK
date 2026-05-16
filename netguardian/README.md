# NetGuardian 2.0 (Advanced Skeleton)

Architektura: `agent -> Kafka -> engine(FastAPI + consumer + detection) -> Redis + TimescaleDB + DuckDB -> response -> dashboard`.

## Uruchomienie

```bash
docker-compose up --build
```

## Dodatkowe komponenty

- CI/CD: `.github/workflows/ci.yml`
- Monitoring: `prometheus/prometheus.yml` + serwisy Prometheus/Grafana
- Testy: `engine/tests/`
- Threat enrichment: `engine/consumer/enrichment.py`
- Notyfikacje: `engine/response/notifiers.py`

## Endpointy

- `GET http://localhost:8000/status`
- `POST http://localhost:8000/unblock/{ip}`
- `GET http://localhost:8000/report`
- `WS ws://localhost:8001/ws`

## Wymagane sekrety

- `ABUSEIPDB_API_KEY`
- `SLACK_WEBHOOK_URL`
- `engine/ssh/id_rsa`


## Uwaga Docker

W sieci `docker-compose` dashboard powinien łączyć się z `ws://engine:8000/ws` (port kontenera),
zaś z hosta lokalnego używaj `ws://localhost:8001/ws`.
