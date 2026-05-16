from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.schemas.common import BudgetRequest
from api.services.budget_service import upsert_budget, budget_status

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.post("")
async def set_budget(req: BudgetRequest, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    if req.tenant_id != tenant_id:
        raise HTTPException(status_code=400, detail="Body tenant_id must match X-Tenant-ID")
    budget = upsert_budget(db, req.tenant_id, req.monthly_budget_usd)
    return {"tenant_id": budget.tenant_id, "monthly_budget_usd": budget.monthly_budget_usd}

@router.get("")
async def get_budget_status(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return budget_status(db, tenant_id)
