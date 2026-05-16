import asyncio
import httpx

async def periodic_sync(main_mcp_url: str, interval: int = 30):
    while True:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(f"{main_mcp_url}/api/op/sync", json={"source_mcp": "op-mcp-1", "events": []})
        except Exception:
            pass
        await asyncio.sleep(interval)
