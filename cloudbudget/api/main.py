from contextlib import asynccontextmanager
from datetime import date, datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_: FastAPI):
    from api.core.database import init_db

    init_db()
    yield


app = FastAPI(title="CloudBudget API", version="1.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "cloudbudget-api",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


COSTS = [
    {"id": 1, "service": "EC2", "amount": 150.0, "date": "2024-01-01"},
    {"id": 2, "service": "RDS", "amount": 200.0, "date": "2024-01-01"},
    {"id": 3, "service": "S3", "amount": 50.0, "date": "2024-01-01"},
    {"id": 4, "service": "Lambda", "amount": 75.0, "date": "2024-01-02"},
]


@app.get("/api/v1/costs")
def get_costs(service: str | None = None) -> list[dict]:
    if not service:
        return COSTS
    return [item for item in COSTS if item["service"].lower() == service.lower()]


@app.get("/api/v1/costs/summary")
def get_costs_summary() -> dict:
    total = sum(item["amount"] for item in COSTS)
    by_service: dict[str, float] = {}
    for item in COSTS:
        by_service[item["service"]] = by_service.get(item["service"], 0.0) + item["amount"]

    start = min(date.fromisoformat(item["date"]) for item in COSTS)
    end = max(date.fromisoformat(item["date"]) for item in COSTS)
    return {
        "currency": "USD",
        "total": round(total, 2),
        "services": by_service,
        "period": {"from": start.isoformat(), "to": end.isoformat()},
    }


@app.get("/api/v1/costs/top")
def get_top_costs(limit: int = 3) -> list[dict]:
    safe_limit = 1 if limit < 1 else min(limit, len(COSTS))
    ranked = sorted(COSTS, key=lambda item: item["amount"], reverse=True)
    return ranked[:safe_limit]
