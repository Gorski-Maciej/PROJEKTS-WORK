from sqlalchemy import String, Float, DateTime, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from api.core.database import Base


class Tenant(Base):
    __tablename__ = "tenants"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)


class Budget(Base):
    __tablename__ = "budgets"
    __table_args__ = (UniqueConstraint("tenant_id", name="uq_budget_tenant"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    monthly_budget_usd: Mapped[float] = mapped_column(Float)


class CostRecord(Base):
    __tablename__ = "cost_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    provider: Mapped[str] = mapped_column(String(32), index=True)
    service: Mapped[str] = mapped_column(String(80), index=True)
    resource_id: Mapped[str] = mapped_column(String(128), index=True)
    amount_usd: Mapped[float] = mapped_column(Float)
    usage_quantity: Mapped[float] = mapped_column(Float, default=0)
    collected_at: Mapped[datetime] = mapped_column(DateTime, index=True)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    category: Mapped[str] = mapped_column(String(50))
    resource_id: Mapped[str] = mapped_column(String(128), index=True)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_savings_usd: Mapped[float] = mapped_column(Float, default=0.0)
    approved: Mapped[bool] = mapped_column(Boolean, default=False)
    note: Mapped[str] = mapped_column(Text, default="")


class ActionLog(Base):
    __tablename__ = "action_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True)
    action: Mapped[str] = mapped_column(String(60), index=True)
    resource_id: Mapped[str] = mapped_column(String(128), index=True)
    approved_by: Mapped[str] = mapped_column(String(120))
    executed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
