from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.services.alerting.alert_service import evaluate_budget_alert

router = APIRouter(prefix="/alerts", tags=["alerts"])


@router.get('/budget/{tenant_id}')
async def budget_alert(tenant_id: int, db: Session = Depends(get_db)) -> dict:
    return evaluate_budget_alert(db, tenant_id)
