# InfraFlow

System monitoringu infrastruktury serwerowej z metrykami time-series i dashboardem operacyjnym.

## Kluczowe funkcje
- Zbieranie metryk hostów i zdarzeń.
- Przetwarzanie kolejkowe (worker).
- Dashboard operacyjny + Grafana/Prometheus.

## Architektura
```text
[Dashboard] --> [Engine API] --> [TimescaleDB]
                    |
                    +--> [Redis Queue] --> [Worker]
```

## Stack
- Python / FastAPI
- Redis
- TimescaleDB (PostgreSQL)
- Docker Compose

## Szybki start
```bash
cp -n .env.example .env
docker compose up -d --build
```
API docs: `http://localhost:8001/docs`
Dashboard: `http://localhost:8081`

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | /docs | Swagger UI |
| GET | /health | Healthcheck API |

## Testy
```bash
pytest -q
```

## Autor
Team DevOps
