from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.services.reconciliation_service import reconcile_invoice_with_costs

router = APIRouter(prefix="/reconciliation", tags=["reconciliation"])


class ReconciliationRequest(BaseModel):
    invoice_total: float = Field(ge=0)
    platform_total: float = Field(ge=0)
    threshold_pct: float = Field(default=1.0, ge=0)


@router.post('')
async def reconcile(req: ReconciliationRequest) -> dict:
    return reconcile_invoice_with_costs(req.invoice_total, req.platform_total, req.threshold_pct)
