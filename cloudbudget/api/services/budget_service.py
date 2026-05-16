from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.entities import Budget, CostRecord
from api.core.metrics import BUDGET_UTILIZATION


def upsert_budget(db: Session, tenant_id: int, monthly_budget_usd: float) -> Budget:
    budget = db.query(Budget).filter(Budget.tenant_id == tenant_id).first()
    if budget is None:
        budget = Budget(tenant_id=tenant_id, monthly_budget_usd=monthly_budget_usd)
        db.add(budget)
    else:
        budget.monthly_budget_usd = monthly_budget_usd
    db.commit()
    db.refresh(budget)
    return budget


def budget_status(db: Session, tenant_id: int) -> dict:
    budget = db.query(Budget).filter(Budget.tenant_id == tenant_id).first()
    spent = db.query(func.coalesce(func.sum(CostRecord.amount_usd), 0)).filter(CostRecord.tenant_id == tenant_id).scalar() or 0.0
    if budget is None:
        BUDGET_UTILIZATION.labels(tenant_id=str(tenant_id)).set(0)
        return {"tenant_id": tenant_id, "configured": False, "spent": float(spent)}
    utilization = (float(spent) / budget.monthly_budget_usd) * 100 if budget.monthly_budget_usd else 0
    BUDGET_UTILIZATION.labels(tenant_id=str(tenant_id)).set(utilization)
    forecast_state = "on_track"
    projected_month_end = spent * 1.1
    if projected_month_end > budget.monthly_budget_usd:
        forecast_state = "at_risk"
    state = "ok"
    if utilization >= 120:
        state = "critical"
    elif utilization >= 100:
        state = "exceeded"
    elif utilization >= 80:
        state = "warning"
    return {
        "tenant_id": tenant_id,
        "configured": True,
        "budget": budget.monthly_budget_usd,
        "spent": float(spent),
        "utilization_pct": round(utilization, 2),
        "state": state,
        "projected_month_end": round(float(projected_month_end), 2),
        "forecast_state": forecast_state,
    }
