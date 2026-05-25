import asyncio
import os
from pathlib import Path

import httpx

from .parsers import auth, nginx

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://localhost:8001")
AGENT_ID = os.getenv("SECLOG_AGENT_ID", "seclog-01")
WATCH_PATHS = [p.strip() for p in os.getenv("SECLOG_WATCH_PATHS", "/var/log/auth.log,/var/log/nginx/access.log").split(",") if p.strip()]

PARSERS = {"auth.log": auth.parse_line, "nginx": nginx.parse_line}


def get_parser_for_path(path: str):
    for key, parser in PARSERS.items():
        if key in path:
            return parser
    return None


async def send_log_event(event_type: str, details: dict):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(f"{OPERATIONAL_MCP_URL}/api/agents/logs", json={"agent_id": AGENT_ID, "type": event_type, "details": details})


async def watch_file(path: str):
    p = Path(path)
    offsets = 0
    print(f"[{AGENT_ID}] tailing {path}")
    while True:
        try:
            if p.exists():
                with p.open("r", errors="ignore") as fh:
                    fh.seek(offsets)
                    new_lines = fh.readlines()
                    offsets = fh.tell()
                parser = get_parser_for_path(path)
                if parser:
                    for line in new_lines:
                        event = parser(line.strip())
                        if event:
                            await send_log_event(event["type"], event["details"])
            await asyncio.sleep(1)
        except Exception as exc:
            await send_log_event("seclog_error", {"path": path, "error": str(exc)})
            await asyncio.sleep(2)


async def main():
    await asyncio.gather(*(watch_file(p) for p in WATCH_PATHS))


if __name__ == "__main__":
    asyncio.run(main())


# backward-compatible alias
parser_for = get_parser_for_path
