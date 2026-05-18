# NetAegis

Dwuwarstwowy system MCP (main + operational) z agentami NetPulse, SecLog i NetConfig.

## Kluczowe funkcje
- Orkiestracja incydentów i polityk.
- Agenci operacyjni do telemetrii i automatyki.
- Frontend operatorski.

## Architektura
```text
[Frontend] --> [main_mcp] <--> [operational_mcp]
                               /      |      \
                        [netpulse] [seclog] [netconfig]
```

## Stack
- Python / FastAPI
- SQLite (lokalnie) + Redis
- Docker Compose

## Szybki start
```bash
cp -n .env.example .env
docker compose up -d --build
```
Main MCP docs: `http://localhost:8400/docs`
Operational MCP docs: `http://localhost:8401/docs`

## API (wybrane endpointy)
| Metoda | Endpoint | Opis |
|---|---|---|
| GET | /api/realtime/health | Health main MCP |
| GET | /api/status/ | Health operational MCP |

## Testy
```bash
pytest -q
```

## Autor
Team DevOps
