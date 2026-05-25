from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Date, Float, Integer, String, create_engine, func, select
from sqlalchemy.orm import declarative_base, sessionmaker

from api.core.config import settings
from api.core.database import init_db

Base = declarative_base()


class Cost(Base):
    __tablename__ = "costs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service = Column(String(120), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)


engine = create_engine(settings.DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    Base.metadata.create_all(bind=engine)
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


@app.get("/api/v1/costs")
def get_costs(service: str | None = None) -> list[dict]:
    with SessionLocal() as session:
        stmt = select(Cost)
        if service:
            stmt = stmt.where(func.lower(Cost.service) == service.lower())
        rows = session.execute(stmt.order_by(Cost.date.desc(), Cost.amount.desc())).scalars().all()
        return [{"id": r.id, "service": r.service, "amount": r.amount, "date": r.date.isoformat()} for r in rows]


@app.get("/api/v1/costs/summary")
def get_costs_summary() -> dict:
    with SessionLocal() as session:
        totals = session.execute(select(func.coalesce(func.sum(Cost.amount), 0.0))).scalar_one()
        grouped = session.execute(select(Cost.service, func.sum(Cost.amount)).group_by(Cost.service)).all()
        start, end = session.execute(select(func.min(Cost.date), func.max(Cost.date))).one()

    return {
        "currency": "USD",
        "total": round(float(totals), 2),
        "services": {service: round(float(amount), 2) for service, amount in grouped},
        "period": {
            "from": start.isoformat() if start else None,
            "to": end.isoformat() if end else None,
        },
    }


@app.get("/api/v1/costs/top")
def get_top_costs(limit: int = Query(default=3, ge=1, le=100)) -> list[dict]:
    with SessionLocal() as session:
        rows = session.execute(select(Cost).order_by(Cost.amount.desc()).limit(limit)).scalars().all()
        return [{"id": r.id, "service": r.service, "amount": r.amount, "date": r.date.isoformat()} for r in rows]
