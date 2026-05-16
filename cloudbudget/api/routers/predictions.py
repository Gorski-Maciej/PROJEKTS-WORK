from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.services.prediction_service import forecast_for_tenant

router = APIRouter(prefix="/predictions", tags=["predictions"])

@router.get("/{tenant_id}")
async def forecast(tenant_id: int, db: Session = Depends(get_db)) -> dict:
    return forecast_for_tenant(db, tenant_id)
