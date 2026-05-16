from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.entities import CostRecord


def cost_summary(db: Session, tenant_id: int) -> dict:
    total = db.query(func.coalesce(func.sum(CostRecord.amount_usd), 0)).filter(CostRecord.tenant_id == tenant_id).scalar()
    grouped = (
        db.query(CostRecord.provider, func.sum(CostRecord.amount_usd))
        .filter(CostRecord.tenant_id == tenant_id)
        .group_by(CostRecord.provider)
        .all()
    )
    return {"tenant_id": tenant_id, "monthly_total": float(total or 0), "by_provider": {p: float(v) for p, v in grouped}}
