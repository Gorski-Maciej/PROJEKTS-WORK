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
