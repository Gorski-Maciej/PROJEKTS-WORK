import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

# Load local .env in development; production can inject env via orchestrator/secrets.
load_dotenv(dotenv_path=Path('/app/.env'), override=False)

app = FastAPI(title="NetAegis NetConfig Agent")


def _required_secret(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value.lower() in {"admin", "change_me_in_production", "change-me"}:
        return ""
    return value


@app.get("/health")
def health() -> dict[str, str | bool]:
    username_ok = bool(_required_secret("NETCONFIG_DEVICE_USERNAME"))
    password_ok = bool(_required_secret("NETCONFIG_DEVICE_PASSWORD"))
    return {
        "status": "ok",
        "service": "netconfig",
        "secrets_configured": username_ok and password_ok,
    }
