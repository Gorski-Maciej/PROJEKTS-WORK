import httpx

class SyncService:
    def __init__(self, main_url: str):
        self.main_url = main_url

    async def sync(self, source_mcp: str, events: list[dict]):
        async with httpx.AsyncClient(timeout=10) as client:
            return await client.post(f"{self.main_url}/api/op/sync", json={"source_mcp": source_mcp, "events": events})
