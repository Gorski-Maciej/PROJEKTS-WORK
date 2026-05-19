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
cp .env.example .env && docker compose up -d
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

## Testy
```bash
pytest -q
```

## Autor
Team DevOps


## GeoIP (opcjonalne)
- Ustaw `SKIP_GEOIP_CHECK=true` dla demo/local bez bazy GeoIP.
- Dla pełnego geo-enrichment zamontuj plik `GeoLite2-City.mmdb` pod ścieżką `GEOIP_DB` (domyślnie `/app/data/GeoLite2-City.mmdb`).
- Przy starcie uruchamiany jest `download_geoip.sh`, który waliduje obecność bazy gdy check nie jest pomijany.
