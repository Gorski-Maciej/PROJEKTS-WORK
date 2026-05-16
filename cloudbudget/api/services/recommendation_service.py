from sqlalchemy.orm import Session
from api.models.entities import CostRecord, Recommendation
from api.core.metrics import RECOMMENDATIONS_TOTAL
from api.services.recommendation_rules import categorize


def generate_recommendations(db: Session, tenant_id: int) -> list[Recommendation]:
    high_spend = db.query(CostRecord).filter(CostRecord.tenant_id == tenant_id, CostRecord.amount_usd > 75).all()
    output: list[Recommendation] = []
    for row in high_spend:
        category, confidence, savings = categorize(row.service, row.amount_usd)
        rec = Recommendation(
            tenant_id=tenant_id,
            category=category,
            resource_id=row.resource_id,
            confidence=confidence,
            estimated_savings_usd=round(savings, 2),
            note=f"Generated from spend and service profile ({row.service}).",
        )
        db.add(rec)
        output.append(rec)
        RECOMMENDATIONS_TOTAL.labels(category=category).inc()
    db.commit()
    return output
