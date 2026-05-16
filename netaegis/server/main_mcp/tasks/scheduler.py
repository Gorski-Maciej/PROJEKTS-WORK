import asyncio
import httpx

async def pull_operational_status(operational_urls: list[str]) -> list[dict]:
    results = []
    async with httpx.AsyncClient(timeout=5) as client:
        for url in operational_urls:
            try:
                r = await client.get(f"{url}/api/agents/")
                results.append({"url": url, "ok": r.status_code == 200, "agents": r.json() if r.status_code == 200 else {}})
            except Exception:
                results.append({"url": url, "ok": False, "agents": {}})
    return results

async def periodic_status_sync(interval: int = 60):
    while True:
        await asyncio.sleep(interval)
