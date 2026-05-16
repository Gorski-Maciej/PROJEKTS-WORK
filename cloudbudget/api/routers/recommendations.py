from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.services.recommendation_service import generate_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("/generate/{tenant_id}")
async def generate(tenant_id: int, db: Session = Depends(get_db)) -> list[dict]:
    recs = generate_recommendations(db, tenant_id)
    return [
        {
            "category": r.category,
            "resource_id": r.resource_id,
            "estimated_savings_usd": r.estimated_savings_usd,
            "confidence": r.confidence,
            "approved": r.approved,
        }
        for r in recs
    ]
