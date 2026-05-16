import asyncio
import httpx
import psutil

OP = "http://localhost:8001"

async def loop():
    async with httpx.AsyncClient() as c:
        await c.post(f"{OP}/api/agents/heartbeat", json={"agent_id": "netpulse-01"})
        while True:
            await c.post(f"{OP}/api/agents/metrics", json={"agent_id": "netpulse-01", "name": "cpu_percent", "value": psutil.cpu_percent(interval=0.2)})
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(loop())
