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
# Netguardian

Projekt netguardian - dokumentacja uruchomienia.

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
API docs: `http://localhost:8300/docs`


## DuckDB storage mode
NetGuardian korzysta z lokalnego pliku DuckDB (`DUCKDB_PATH`) montowanego przez wolumen `duckdb_data:/data`.
Nie jest wymagany osobny serwis `duckdb-api`, ponieważ aplikacja łączy się bezpośrednio z plikiem bazy.

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | /docs | Swagger UI |
| WS | /ws | Strumień zdarzeń |

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
