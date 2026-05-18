# CloudBudget

Platforma FinOps do analizy kosztów chmury, prognozowania i automatyzacji rekomendacji oszczędności.

## Kluczowe funkcje
- Agregacja kosztów i raportowanie trendów.
- API do rekomendacji optymalizacyjnych i chargeback.
- Kolejki asynchroniczne (Celery + RabbitMQ) dla zadań analitycznych.
- Dashboard frontend do podglądu metryk.

## Architektura
```text
[Frontend] ---> [FastAPI API] ---> [PostgreSQL]
                    |   \
                    |    ---> [DuckDB analytics]
                    ---> [Redis] + [RabbitMQ/Celery Worker]
```

## Stack
- Python / FastAPI
- PostgreSQL + DuckDB
- Redis + RabbitMQ + Celery
- Docker Compose

## Szybki start
# Cloudbudget

Projekt cloudbudget - dokumentacja uruchomienia.

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
API docs: `http://localhost:8100/docs`

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | / | Health root |
| GET | /docs | Swagger UI |
| GET | /api/v1/health | Stan API |

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
