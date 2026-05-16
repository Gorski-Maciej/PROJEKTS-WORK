import asyncio
from pathlib import Path
import httpx
from jinja2 import Environment, FileSystemLoader

AGENT_ID = "netconfig-01"
OP_URL = "http://localhost:8001"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_template(template_name: str, context: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_name)
    return template.render(context)


async def notify(message: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{OP_URL}/api/agents/logs",
            json={"agent_id": AGENT_ID, "type": "config_status", "details": {"message": message}},
        )


async def main():
    cfg = render_template("mikrotik_acl.j2", {"admin_ip": "10.10.10.10"})
    out = Path("./rendered_mikrotik_acl.txt")
    out.write_text(cfg)
    await notify(f"rendered_template:{out}")


if __name__ == "__main__":
    asyncio.run(main())
