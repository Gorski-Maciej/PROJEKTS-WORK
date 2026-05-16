from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from api.models.entities import Recommendation
from api.services.actions.action_service import create_action_request


@dataclass
class AutopilotCandidate:
    recommendation_id: int
    category: str
    resource_id: str
    confidence: float
    estimated_savings_usd: float


def eligible_autopilot_recommendations(
    db: Session,
    tenant_id: int,
    min_confidence: float = 0.9,
    min_savings: float = 50.0,
) -> list[Recommendation]:
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


def _map_category_to_action(category: str) -> str:
    mapping = {
        "rightsizing": "resize_instance",
        "idle_resource": "stop_instance",
        "unused_storage": "delete_volume",
        "savings_plan": "purchase_savings_plan",
    }
    return mapping.get(category, "review_recommendation")


def apply_autopilot_plan(
    db: Session,
    tenant_id: int,
    recommendation_ids: list[int],
    requested_by: str = "autopilot",
    reason_prefix: str = "Autopilot candidate",
) -> dict:
    if not recommendation_ids:
        return {"tenant_id": tenant_id, "approved_count": 0, "action_requests": []}

    rows = (
        db.query(Recommendation)
        .filter(
            Recommendation.tenant_id == tenant_id,
            Recommendation.id.in_(recommendation_ids),
        )
        .all()
    )

    action_requests: list[dict] = []
    for row in rows:
        row.approved = True
        action = _map_category_to_action(row.category)
        req = create_action_request(
            db,
            tenant_id=tenant_id,
            action=action,
            resource_id=row.resource_id,
            requested_by=requested_by,
            reason=f"{reason_prefix}: rec#{row.id} savings={row.estimated_savings_usd}",
        )
        action_requests.append({"recommendation_id": row.id, **req, "action": action, "resource_id": row.resource_id})

    db.commit()
    return {"tenant_id": tenant_id, "approved_count": len(rows), "action_requests": action_requests}
