from sqlalchemy.orm import Session
from api.models.entities import Recommendation


def eligible_autopilot_recommendations(db: Session, tenant_id: int, min_confidence: float = 0.9, min_savings: float = 50.0) -> list[Recommendation]:
    return (
        db.query(Recommendation)
        .filter(
            Recommendation.tenant_id == tenant_id,
            Recommendation.approved.is_(False),
            Recommendation.confidence >= min_confidence,
            Recommendation.estimated_savings_usd >= min_savings,
        )
        .all()
    )


def mark_recommendations_approved(db: Session, tenant_id: int, recommendation_ids: list[int]) -> int:
    if not recommendation_ids:
        return 0
    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.tenant_id == tenant_id,
            Recommendation.id.in_(recommendation_ids),
        )
        .all()
    )
    for row in rows:
        row.approved = True
    db.commit()
    return len(rows)
