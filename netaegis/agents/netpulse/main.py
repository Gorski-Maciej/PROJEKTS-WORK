import asyncio
import os
from datetime import datetime, timezone

import httpx
from fastapi import FastAPI

app = FastAPI(title="NetAegis NetPulse Agent", version="1.1.0")

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://operational_mcp:8001")
AGENT_ID = os.getenv("NETPULSE_AGENT_ID", "netpulse-01")
INTERVAL = int(os.getenv("NETPULSE_INTERVAL", "30"))
GATEWAY_IP = os.getenv("NETPULSE_GATEWAY_IP", "192.168.1.1")


async def ping_gateway(ip: str) -> bool:
    proc = await asyncio.create_subprocess_exec(
        "ping", "-c", "1", "-W", "2", ip,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL,
    )
    return (await proc.wait()) == 0


async def send_metric(name: str, value: float):
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/metrics",
            json={"agent_id": AGENT_ID, "name": name, "value": value},
        )


async def send_alert(message: str):
    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/logs",
            json={"agent_id": AGENT_ID, "type": "netpulse_alert", "details": {"message": message, "gateway": GATEWAY_IP}},
        )


async def monitor_loop():
    while True:
        try:
            ok = await ping_gateway(GATEWAY_IP)
            await send_metric("ping_gateway_up", 1 if ok else 0)
            if not ok:
                await send_alert("Gateway ping failed")
        except Exception as exc:
            await send_alert(f"NetPulse monitor error: {exc}")
        await asyncio.sleep(INTERVAL)


@app.on_event("startup")
async def _startup() -> None:
    asyncio.create_task(monitor_loop())


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "netpulse", "timestamp": datetime.now(timezone.utc).isoformat()}
