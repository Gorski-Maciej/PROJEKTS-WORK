# NetGuardian

Platforma cybersec do detekcji zdarzeń sieciowych, korelacji i automatyzacji reakcji.

## Kluczowe funkcje
- Ingest zdarzeń przez Kafka.
- Analiza behawioralna i regułowa.
- Dashboard i metryki operacyjne.

## Architektura
```text
[Agent] --> [Kafka] --> [Engine API] --> [TimescaleDB + DuckDB]
                             |
                             +--> [Redis]
[Dashboard] <----------------+
```

## Stack
- Python / FastAPI
- Kafka + Zookeeper
- Redis + TimescaleDB + DuckDB
- Docker Compose

## Szybki start
```bash
cp -n .env.example .env
docker compose up -d --build
```
API docs: `http://localhost:8300/docs`

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | /docs | Swagger UI |
| WS | /ws | Strumień zdarzeń |

## Testy
```bash
pytest -q
```

## Autor
Team DevOps
