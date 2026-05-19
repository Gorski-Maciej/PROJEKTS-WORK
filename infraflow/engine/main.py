import os
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

CONFIG_PATH = Path(os.getenv("CONFIG_PATH", "/app/config/servers.yml"))


class RunbookRequest(BaseModel):
    server: str = Field(min_length=1)
    action: str = Field(min_length=1)


def _initialize_state() -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("servers:\n", encoding="utf-8")


@asynccontextmanager
async def lifespan(_: FastAPI):
    _initialize_state()
    yield


app = FastAPI(title="InfraFlow API", version="1.1.0", lifespan=lifespan)


def _parse_scalar(value: str):
    raw = value.strip().strip('"').strip("'")
    if raw.lower() in {"true", "false"}:
        return raw.lower() == "true"
    if raw.isdigit():
        return int(raw)
    return raw


def _parse_servers_yaml(content: str) -> list[dict]:
    """Parse a narrow YAML subset used in infraflow server config files."""
    servers: list[dict] = []
    current: dict | None = None
    in_servers = False

    for raw in content.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "servers:":
            in_servers = True
            continue
        if not in_servers:
            continue
        if stripped.startswith("- "):
            if current:
                servers.append(current)
            current = {}
            rest = stripped[2:].strip()
            if rest and ":" in rest:
                key, value = rest.split(":", 1)
                current[key.strip()] = _parse_scalar(value)
            continue
        if current is not None and ":" in stripped:
            key, value = stripped.split(":", 1)
            current[key.strip()] = _parse_scalar(value)

    if current:
        servers.append(current)
    return servers


def _load_servers() -> list[dict]:
    if not CONFIG_PATH.exists():
        return []
    content = CONFIG_PATH.read_text(encoding="utf-8")
    return _parse_servers_yaml(content)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "infraflow-engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/servers")
def list_servers() -> list[dict]:
    return _load_servers()


@app.get("/api/v1/servers/{server_name}")
def get_server(server_name: str) -> dict:
    servers = _load_servers()
    for server in servers:
        if server.get("name") == server_name:
            return server
    raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")


@app.post("/api/v1/runbooks/execute")
def execute_runbook(request: RunbookRequest) -> dict:
    exists = any(s.get("name") == request.server for s in _load_servers())
    if not exists:
        raise HTTPException(status_code=404, detail="Unknown server")

    return {
        "status": "scheduled",
        "server": request.server,
        "action": request.action,
        "scheduled_at": datetime.now(timezone.utc).isoformat(),
    }
