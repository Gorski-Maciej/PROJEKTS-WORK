import asyncio
import httpx
from agents.seclog.parsers.auth import parse_line as parse_auth
from agents.seclog.parsers.nginx import parse_line as parse_nginx

OPERATIONAL_MCP_URL = "http://localhost:8001"
AGENT_ID = "seclog-01"

SAMPLES = [
    "Failed password for root from 10.0.0.2 port 22 ssh2",
    "127.0.0.1 - - [12/Jan/2026] \"GET /health HTTP/1.1\" 503 123",
]


async def send_event(event: dict):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/logs",
            json={"agent_id": AGENT_ID, "type": event["type"], "details": event["details"]},
        )


async def main():
    for line in SAMPLES:
        event = parse_auth(line) or parse_nginx(line)
        if event:
            await send_event(event)


if __name__ == "__main__":
    asyncio.run(main())
