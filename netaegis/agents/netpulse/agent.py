import asyncio
import os

import httpx
import psutil

from .checks import check_port, ping_host

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://localhost:8001")
AGENT_ID = os.getenv("NETPULSE_AGENT_ID", "netpulse-01")
INTERVAL = int(os.getenv("NETPULSE_INTERVAL", "30"))
GATEWAY_IP = os.getenv("NETPULSE_GATEWAY_IP", "192.168.1.1")
APP_HOST = os.getenv("NETPULSE_APP_HOST", "192.168.1.10")
APP_PORT = int(os.getenv("NETPULSE_APP_PORT", "80"))


async def collect_metrics() -> list[dict]:
    metrics: list[dict] = []

    rtt = ping_host(GATEWAY_IP)
    if rtt is not None:
        metrics.append({"name": "ping_gateway_ms", "value": rtt})

    http_ok = check_port(APP_HOST, APP_PORT)
    metrics.append({"name": "http_port_open", "value": 1 if http_ok else 0})
    metrics.append({"name": "cpu_percent", "value": psutil.cpu_percent(interval=1)})
    metrics.append({"name": "memory_percent", "value": psutil.virtual_memory().percent})

    return metrics


async def send_metrics(metrics: list[dict]):
    async with httpx.AsyncClient(timeout=10) as client:
        for metric in metrics:
            await client.post(
                f"{OPERATIONAL_MCP_URL}/api/agents/metrics",
                json={"agent_id": AGENT_ID, "name": metric["name"], "value": metric["value"]},
            )


async def register_heartbeat():
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/heartbeat",
            json={"agent_id": AGENT_ID, "name": "NetPulse Agent"},
        )


async def main():
    print(f"[{AGENT_ID}] started; interval={INTERVAL}s; target={OPERATIONAL_MCP_URL}")
    await register_heartbeat()
    while True:
        try:
            metrics = await collect_metrics()
            await send_metrics(metrics)
            print(f"[{AGENT_ID}] sent {len(metrics)} metrics")
        except Exception as exc:
            print(f"[{AGENT_ID}] error: {exc}")
        await asyncio.sleep(INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
