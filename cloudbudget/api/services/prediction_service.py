from sqlalchemy.orm import Session
from api.models.entities import CostRecord
from ml.prophet_forecaster import forecast_monthly_cost


def forecast_for_tenant(db: Session, tenant_id: int) -> dict:
    rows = db.query(CostRecord).filter(CostRecord.tenant_id == tenant_id).all()
    history = [{"amount_usd": r.amount_usd, "collected_at": r.collected_at} for r in rows]
    return {"tenant_id": tenant_id, **forecast_monthly_cost(history)}
