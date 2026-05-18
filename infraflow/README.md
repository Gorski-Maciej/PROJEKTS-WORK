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
# Infraflow

Projekt infraflow - dokumentacja uruchomienia.

## Funkcje
- API
- Dashboard
- Kolejki i baza danych

## Architektura
```
[Client] -> [API] -> [DB/Cache/Queue]
```

## Stack
Python, FastAPI, Docker Compose

## Quick start
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

## Endpointy
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | /docs | Swagger UI |

## Testy
```bash
pytest -q
```

## Autor
Team DevOps
