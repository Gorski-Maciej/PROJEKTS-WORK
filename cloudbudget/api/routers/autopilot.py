from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.autopilot_service import eligible_autopilot_recommendations, apply_autopilot_plan

router = APIRouter(prefix="/autopilot", tags=["autopilot"])


class AutopilotApplyRequest(BaseModel):
    recommendation_ids: list[int] = Field(default_factory=list)
    requested_by: str = Field(default="autopilot")


@router.get('/eligible')
async def eligible(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> list[dict]:
    rows = eligible_autopilot_recommendations(db, tenant_id)
    return [
        {
            "id": r.id,
            "resource_id": r.resource_id,
            "category": r.category,
            "confidence": r.confidence,
            "estimated_savings_usd": r.estimated_savings_usd,
        }
        for r in rows
    ]


@router.post('/apply')
async def apply(req: AutopilotApplyRequest, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return apply_autopilot_plan(db, tenant_id, req.recommendation_ids, requested_by=req.requested_by)
