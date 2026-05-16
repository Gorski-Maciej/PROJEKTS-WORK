import asyncio
import os
from pathlib import Path

import httpx
from watchfiles import awatch

from .parsers import auth, nginx

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://localhost:8001")
AGENT_ID = os.getenv("SECLOG_AGENT_ID", "seclog-01")
WATCH_PATHS = [
    p.strip() for p in os.getenv("SECLOG_WATCH_PATHS", "/var/log/auth.log,/var/log/nginx/access.log").split(",") if p.strip()
]

PARSERS = {
    "auth.log": auth.parse_line,
    "nginx": nginx.parse_line,
}


def get_parser_for_path(path: str):
    for key, parser in PARSERS.items():
        if key in path:
            return parser
    return None


async def send_log_event(event_type: str, details: dict):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/logs",
            json={"agent_id": AGENT_ID, "type": event_type, "details": details},
        )


async def main():
    print(f"[{AGENT_ID}] watching: {WATCH_PATHS}")
    async for changes in awatch(*WATCH_PATHS):
        for _change_type, path in changes:
            parser = get_parser_for_path(path)
            if parser is None:
                continue
            p = Path(path)
            if not p.exists():
                continue
            try:
                lines = p.read_text().splitlines()
                if not lines:
                    continue
                event = parser(lines[-1])
                if event:
                    await send_log_event(event["type"], event["details"])
                    print(f"[{AGENT_ID}] event: {event['type']}")
            except Exception as exc:
                print(f"[{AGENT_ID}] read error {path}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
