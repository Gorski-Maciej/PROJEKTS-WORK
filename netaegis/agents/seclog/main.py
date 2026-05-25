import asyncio
import os
from datetime import datetime, timezone
from pathlib import Path

import httpx
from fastapi import FastAPI

app = FastAPI(title="NetAegis SecLog Agent", version="1.1.0")

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://operational_mcp:8001")
AGENT_ID = os.getenv("SECLOG_AGENT_ID", "seclog-01")
WATCH_PATHS = [
    p.strip()
    for p in os.getenv("SECLOG_WATCH_PATHS", "/var/log/auth.log,/var/log/nginx/access.log").split(",")
    if p.strip()
]


async def send_log_event(path: str, line: str):
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/logs",
            json={
                "agent_id": AGENT_ID,
                "type": "seclog_line",
                "details": {"path": path, "line": line},
            },
        )


async def tail_file(path: str):
    p = Path(path)
    offset = 0
    while True:
        try:
            if p.exists():
                with p.open("r", errors="ignore") as fh:
                    fh.seek(offset)
                    lines = fh.readlines()
                    offset = fh.tell()
                for line in lines:
                    line = line.strip()
                    if line:
                        await send_log_event(path, line)
            await asyncio.sleep(1)
        except Exception as exc:
            await send_log_event(path, f"seclog_error: {exc}")
            await asyncio.sleep(2)


@app.on_event("startup")
async def _startup() -> None:
    for path in WATCH_PATHS:
        asyncio.create_task(tail_file(path))


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "seclog",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/status")
def status() -> dict:
    return {"agent": "seclog", "state": "watching", "paths": WATCH_PATHS}
