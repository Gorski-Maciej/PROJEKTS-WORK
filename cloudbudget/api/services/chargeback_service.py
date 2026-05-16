from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.entities import CostRecord


def showback_by_provider(db: Session, tenant_id: int) -> list[dict]:
    rows = (
        db.query(CostRecord.provider, func.sum(CostRecord.amount_usd))
        .filter(CostRecord.tenant_id == tenant_id)
        .group_by(CostRecord.provider)
        .all()
    )
    return [{"provider": provider, "amount_usd": round(float(total or 0), 2)} for provider, total in rows]


def chargeback_by_service(db: Session, tenant_id: int) -> list[dict]:
    rows = (
        db.query(CostRecord.service, func.sum(CostRecord.amount_usd))
        .filter(CostRecord.tenant_id == tenant_id)
        .group_by(CostRecord.service)
        .all()
    )
    return [{"service": service, "amount_usd": round(float(total or 0), 2)} for service, total in rows]
