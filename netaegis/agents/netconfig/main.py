import os
from datetime import datetime, timezone
from pathlib import Path


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

LOCAL_REPO = Path(os.getenv("NETCONFIG_LOCAL_REPO", "./configs"))

app = FastAPI(title="NetAegis NetConfig Agent", version="1.1.0")


class ConfigPayload(BaseModel):
    filename: str
    content: str


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "netconfig", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/v1/status")
def status() -> dict:
    return {"agent": "netconfig", "state": "ready", "repo": str(LOCAL_REPO)}


@app.post("/api/v1/apply-config")
def apply_config(payload: ConfigPayload) -> dict:
    filename = payload.filename.strip()
    candidate = Path(filename)
    if (
        not filename
        or filename.startswith(".")
        or filename != candidate.name
        or ".." in candidate.parts
        or "\\" in filename
    ):
        raise HTTPException(status_code=400, detail="Invalid filename")
    LOCAL_REPO.mkdir(parents=True, exist_ok=True)
    target = LOCAL_REPO / filename
    target.write_text(payload.content)
    return {"status": "applied", "path": str(target)}
