import os
from contextlib import asynccontextmanager
from pathlib import Path
from datetime import datetime, timezone
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

DUCKDB_PATH = Path(os.getenv("DUCKDB_PATH", "/tmp/netguardian.db"))


def _initialize_state() -> None:
    DUCKDB_PATH.parent.mkdir(parents=True, exist_ok=True)
    DUCKDB_PATH.touch(exist_ok=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    _initialize_state()
    yield


app = FastAPI(title="NetGuardian API", version="1.1.0", lifespan=lifespan)


class AlertIn(BaseModel):
    message: str = Field(min_length=5)
    severity: Literal["low", "medium", "high", "critical"] = "medium"
    source_ip: str | None = None


ALERTS: list[dict] = [
    {"id": 1, "message": "DDoS attack detected", "severity": "high", "source_ip": "10.0.0.7"},
    {"id": 2, "message": "Port scan from 10.0.0.5", "severity": "medium", "source_ip": "10.0.0.5"},
]


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "netguardian-engine",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/v1/alerts")
def get_alerts(min_severity: Literal["low", "medium", "high", "critical"] | None = None) -> list[dict]:
    if not min_severity:
        return ALERTS
    order = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    threshold = order[min_severity]
    return [a for a in ALERTS if order.get(a["severity"], 1) >= threshold]


@app.post("/api/v1/alerts")
def create_alert(alert: AlertIn) -> dict:
    new_id = max((a["id"] for a in ALERTS), default=0) + 1
    payload = {
        "id": new_id,
        "message": alert.message,
        "severity": alert.severity,
        "source_ip": alert.source_ip,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    ALERTS.append(payload)
    return payload
