import os
from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="NetAegis Main MCP", version="1.1.0")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "main_mcp",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/status")
def status() -> dict:
    return {
        "mcp": "ready",
        "mode": os.getenv("NETAEGIS_MODE", "standalone"),
        "main_mcp_url": os.getenv("MAIN_MCP_URL", "http://main_mcp:8000"),
    }


@app.get("/api/v1/components")
def components() -> dict:
    return {
        "main_mcp": {"enabled": True, "url": os.getenv("MAIN_MCP_URL", "http://main_mcp:8000")},
        "operational_mcp": {"enabled": True, "url": os.getenv("OPERATIONAL_MCP_URL", "http://operational_mcp:8001")},
        "redis": {"enabled": True, "url": os.getenv("REDIS_URL", "redis://redis:6379/0")},
    }
