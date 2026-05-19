from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI

app = FastAPI(title="InfraFlow API")
servers: list[dict[str, Any]] = []


@app.on_event("startup")
def load_servers() -> None:
    global servers
    path = Path("/app/config/servers.yml")
    if path.exists():
        content = yaml.safe_load(path.read_text()) or {}
        servers = content.get("servers", []) if isinstance(content, dict) else []
    else:
        servers = []


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "infraflow-engine"}


@app.get("/api/v1/servers")
def get_servers() -> dict[str, list[dict[str, Any]]]:
    return {"servers": servers}
