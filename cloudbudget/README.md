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


## Zmienne środowiskowe (nowe/istotne)
- `JWT_SECRET` (min. 32 znaki, wymagany do walidacji tokenów).
- `DUCKDB_PATH` (ścieżka do pliku DuckDB, domyślnie `/data/cloudbudget.duckdb`).

## Uwierzytelnianie
- `POST /auth/login` (demo): `username=demo`, `password=demo` zwraca bearer token JWT.
- Endpointy chronione (np. `/api/v1/costs`, `/api/v1/recommendations`) wymagają nagłówka `Authorization: Bearer <token>`.

## Troubleshooting
- Błąd `Missing token`/`Invalid token`: wygeneruj token przez `/auth/login` i upewnij się, że `JWT_SECRET` jest spójny.
- Błąd walidacji env: uruchom `make validate-env` i ustaw `JWT_SECRET` > 32 znaków.
