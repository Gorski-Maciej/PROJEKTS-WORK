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
cp .env.example .env && docker compose up -d
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


## Zmienne środowiskowe (nowe/istotne)
- `NETCONFIG_DEVICE_USERNAME=CHANGE_ME`
- `NETCONFIG_DEVICE_PASSWORD=CHANGE_ME`
- Ustaw bezpieczne wartości w lokalnym `.env` (bez hardcoded defaultów typu `admin/admin`).

## Wolumeny agentów
- `agent_configs:/app/.agent-configs` (netpulse, seclog)
- `seclog_cache:/app/cache` (seclog)
- `netconfig_local:/app/.agent-configs` (netconfig)

## Endpointy / health
- Main MCP: `GET /api/realtime/health`
- Operational MCP: `GET /api/status/`

## Troubleshooting
- Jeśli agent nie startuje, sprawdź, czy wolumeny named volumes są utworzone i podpięte.
- Przy błędach NetConfig zweryfikuj zmienne `NETCONFIG_DEVICE_*` w `.env`.
