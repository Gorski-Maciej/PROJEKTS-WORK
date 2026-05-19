from __future__ import annotations

import os
from typing import Any

import duckdb
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

app = FastAPI(title="CloudBudget API")

DUCKDB_CONN: duckdb.DuckDBPyConnection | None = None
PG_ENGINE: AsyncEngine | None = None


class RecommendationRequest(BaseModel):
    service: str
    monthly_cost: float


def require_demo_token(authorization: str = Header(default="")) -> str:
    if authorization != "Bearer demo":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return "demo"


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
    try:
        async with PG_ENGINE.connect() as conn:
            await conn.execute(text("SELECT 1"))
    except Exception:
        # Demo mode: allow startup even when Postgres is not yet reachable.
        pass


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "cloudbudget-api"}


@app.get("/api/v1/costs")
async def get_costs(_: str = Depends(require_demo_token)) -> dict[str, Any]:
    rows = DUCKDB_CONN.execute("SELECT service, monthly_cost FROM costs").fetchall() if DUCKDB_CONN else []
    return {
        "items": [
            {"service": row[0], "monthly_cost": row[1]} for row in rows
        ]
    }


@app.post("/api/v1/recommendations")
async def create_recommendation(
    payload: RecommendationRequest,
    _: str = Depends(require_demo_token),
) -> dict[str, Any]:
    suggested = round(payload.monthly_cost * 0.15, 2)
    return {
        "service": payload.service,
        "recommendation": f"Potential monthly savings: ${suggested}",
    }
