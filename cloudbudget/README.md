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
```bash
cp .env.example .env && docker compose up -d
```
API docs: `http://localhost:8100/docs`

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | / | Health root |
| GET | /docs | Swagger UI |
| GET | /api/v1/health | Stan API |

## Testy
```bash
pytest -q
```

## Autor
Team DevOps
