from __future__ import annotations

import asyncio
import os
from typing import Any

import duckdb
from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from api.core.security import create_access_token, verify_access_token

app = FastAPI(title="CloudBudget API")

DUCKDB_CONN: duckdb.DuckDBPyConnection | None = None
PG_ENGINE: AsyncEngine | None = None

class RecommendationRequest(BaseModel):
    service: str
    monthly_cost: float


class LoginRequest(BaseModel):
    username: str = "demo"
    password: str = "demo"


def require_jwt_token(authorization: str = Header(default="")) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    token = authorization.removeprefix("Bearer ").strip()
    payload = verify_access_token(token)
    return str(payload.get("sub", "unknown"))


@app.post("/auth/login")
async def login(payload: LoginRequest) -> dict[str, str]:
    if payload.username != "demo" or payload.password != "demo":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": create_access_token(subject=payload.username, tenant_id=0), "token_type": "bearer"}


@app.on_event("startup")
async def startup() -> None:
    global DUCKDB_CONN, PG_ENGINE

    duckdb_path = os.getenv("DUCKDB_PATH", "/tmp/cloudbudget.duckdb")
    DUCKDB_CONN = duckdb.connect(duckdb_path)
    DUCKDB_CONN.execute(
        "CREATE TABLE IF NOT EXISTS costs(service VARCHAR, monthly_cost DOUBLE)"
    )
    if DUCKDB_CONN.execute("SELECT COUNT(*) FROM costs").fetchone()[0] == 0:
        DUCKDB_CONN.executemany(
            "INSERT INTO costs VALUES (?, ?)",
            [("EC2", 320.5), ("S3", 95.2), ("RDS", 210.1)],
        )

    pg_url = os.getenv(
        "POSTGRES_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/cloudbudget",
    )
    PG_ENGINE = create_async_engine(pg_url, echo=False)
    for attempt in range(1, 6):
        try:
            async with PG_ENGINE.connect() as conn:
                await conn.execute(text("SELECT 1"))
            break
        except Exception:
            if attempt == 5:
                break
            await asyncio.sleep(1.5)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1/costs")
async def get_costs(_: str = Depends(require_jwt_token)) -> dict[str, Any]:
    rows = DUCKDB_CONN.execute("SELECT service, monthly_cost FROM costs").fetchall() if DUCKDB_CONN else []
    return {"items": [{"service": row[0], "monthly_cost": row[1]} for row in rows]}




@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok", "service": "cloudbudget"}


@app.get("/api/v1/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> PlainTextResponse:
    return PlainTextResponse("cloudbudget_requests_total 1\n")


@app.get("/api/v1/costs/summary")
async def costs_summary(x_tenant_id: str = Header(default="")) -> dict[str, str]:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="Missing X-Tenant-ID")
    return {"tenant_id": x_tenant_id, "status": "ok"}

@app.post("/api/v1/recommendations")
async def create_recommendation(
    payload: RecommendationRequest,
    _: str = Depends(require_jwt_token),
) -> dict[str, Any]:
    suggested = round(payload.monthly_cost * 0.15, 2)
    return {
        "service": payload.service,
        "recommendation": f"Potential monthly savings: ${suggested}",
    }
