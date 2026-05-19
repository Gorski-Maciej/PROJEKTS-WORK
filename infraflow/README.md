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
cp .env.example .env && docker compose up -d
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


## Zmienne środowiskowe (nowe/istotne)
- `JWT_SECRET` (min. 32 znaki).
- `DATABASE_URL`, `REDIS_HOST`, `CONFIG_PATH`.

## Kolejność uruchamiania
- `engine` i `worker` startują po `redis` i `timescaledb` (`depends_on.condition: service_healthy`).
- `worker` ma healthcheck Redis z `timeout: 10s`.

## Troubleshooting
- Jeśli worker jest `unhealthy`, sprawdź połączenie do Redis (`docker compose logs worker`).
- Jeśli API nie startuje, zweryfikuj `.env` i `JWT_SECRET` przez `make validate-env`.
