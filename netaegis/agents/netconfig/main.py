from datetime import datetime, timezone

from fastapi import FastAPI

app = FastAPI(title="NetAegis NetConfig Agent", version="1.1.0")


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "netconfig",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/status")
def status() -> dict:
    return {"agent": "netconfig", "state": "ready"}
