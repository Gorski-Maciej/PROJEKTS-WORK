from datetime import date

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.invoice_reconciliation_service import reconcile_invoice_text

router = APIRouter(prefix="/invoice-reconciliation", tags=["invoice-reconciliation"])


class InvoiceReconciliationRequest(BaseModel):
    invoice_text: str
    threshold_pct: float = Field(default=1.0, ge=0)
    start_date: date | None = None
    end_date: date | None = None


@router.post('')
async def reconcile_invoice(
    req: InvoiceReconciliationRequest,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
) -> dict:
    return reconcile_invoice_text(
        db,
        tenant_id,
        req.invoice_text,
        req.threshold_pct,
        start_date=req.start_date,
        end_date=req.end_date,
    )
