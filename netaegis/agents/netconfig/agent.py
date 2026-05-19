import asyncio
import os
from pathlib import Path

import httpx
import paramiko
from git import Repo
from jinja2 import Environment, FileSystemLoader

OPERATIONAL_MCP_URL = os.getenv("OPERATIONAL_MCP_URL", "http://localhost:8001")
AGENT_ID = os.getenv("NETCONFIG_AGENT_ID", "netconfig-01")
LOCAL_REPO = Path(os.getenv("NETCONFIG_LOCAL_REPO", "./configs"))
TEMPLATES_DIR = Path(__file__).parent / "templates"
DEVICE_IP = os.getenv("NETCONFIG_DEVICE_IP", "192.168.1.1")
DEVICE_USERNAME = os.getenv("NETCONFIG_DEVICE_USERNAME", "")
DEVICE_PASSWORD = os.getenv("NETCONFIG_DEVICE_PASSWORD", "")


def render_template(template_name: str, context: dict) -> str:
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_name)
    return template.render(context)


async def send_status(message: str):
    async with httpx.AsyncClient(timeout=10) as client:
        await client.post(
            f"{OPERATIONAL_MCP_URL}/api/agents/logs",
            json={"agent_id": AGENT_ID, "type": "config_status", "details": {"message": message}},
        )


async def collect_config(device_ip: str, username: str, password: str) -> str:
    username = username or DEVICE_USERNAME
    password = password or DEVICE_PASSWORD
    if not username or not password:
        raise ValueError("Missing NETCONFIG_DEVICE_USERNAME or NETCONFIG_DEVICE_PASSWORD")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device_ip, username=username, password=password, timeout=10)
    _, stdout, _ = ssh.exec_command("show running-config")
    content = stdout.read().decode()
    ssh.close()
    return content


async def push_config(device_ip: str, config: str, username: str | None = None, password: str | None = None):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(device_ip, username=username, password=password, timeout=10)
    ssh.exec_command("configure terminal")
    for line in config.splitlines():
        if line.strip():
            ssh.exec_command(line)
    ssh.exec_command("end")
    ssh.close()


async def main():
    LOCAL_REPO.mkdir(parents=True, exist_ok=True)
    repo = Repo.init(LOCAL_REPO) if not (LOCAL_REPO / ".git").exists() else Repo(LOCAL_REPO)

    if repo.head.is_detached or not repo.head.is_valid():
        await send_status("git repo initialized")

    template_render = render_template("mikrotik_acl.j2", {"admin_ip": "10.10.10.10"})
    rendered_file = LOCAL_REPO / "rendered_mikrotik_acl.txt"
    rendered_file.write_text(template_render)

    try:
        if not DEVICE_USERNAME or not DEVICE_PASSWORD:
            raise ValueError("Missing NETCONFIG_DEVICE_USERNAME or NETCONFIG_DEVICE_PASSWORD")
        config = await collect_config(DEVICE_IP, DEVICE_USERNAME, DEVICE_PASSWORD)
        config_file = LOCAL_REPO / "router_config.txt"
        config_file.write_text(config)

        repo.index.add([str(rendered_file), str(config_file)])
        repo.index.commit("automatic config backup")
        await send_status(f"config backup committed: {repo.head.commit.hexsha[:7]}")
    except Exception as exc:
        await send_status(f"config collection failed: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
