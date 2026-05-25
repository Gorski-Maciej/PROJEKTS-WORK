import asyncio
import os

import httpx

from .checks import ping_host

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://localhost:8001")
AGENT_ID = os.getenv("NETPULSE_AGENT_ID", "netpulse-01")
INTERVAL = int(os.getenv("NETPULSE_INTERVAL", "30"))
GATEWAY_IP = os.getenv("NETPULSE_GATEWAY_IP", "192.168.1.1")


async def send_metric(name: str, value: float):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{OPERATIONAL_MCP_URL}/api/agents/metrics", json={"agent_id": AGENT_ID, "name": name, "value": value})


async def send_alert(message: str):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{OPERATIONAL_MCP_URL}/api/agents/logs", json={"agent_id": AGENT_ID, "type": "netpulse_alert", "details": {"message": message, "gateway": GATEWAY_IP}})


async def monitor_loop():
    print(f"[{AGENT_ID}] monitoring gateway={GATEWAY_IP} every {INTERVAL}s")
    while True:
        try:
            rtt = ping_host(GATEWAY_IP)
            if rtt is None:
                await send_metric("ping_gateway_up", 0)
                await send_alert("Gateway ping failed")
            else:
                await send_metric("ping_gateway_up", 1)
                await send_metric("ping_gateway_ms", float(rtt))
        except Exception as exc:
            await send_alert(f"Monitor error: {exc}")
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(monitor_loop())
