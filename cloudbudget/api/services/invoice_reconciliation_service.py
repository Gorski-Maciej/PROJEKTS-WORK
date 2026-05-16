from sqlalchemy.orm import Session
from sqlalchemy import func
from api.models.entities import CostRecord
from api.services.ocr.invoice_service import parse_invoice_text
from api.services.reconciliation_service import reconcile_invoice_with_costs


def reconcile_invoice_text(db: Session, tenant_id: int, invoice_text: str, threshold_pct: float = 1.0) -> dict:
    parsed = parse_invoice_text(invoice_text)
    platform_total = (
        db.query(func.coalesce(func.sum(CostRecord.amount_usd), 0))
        .filter(CostRecord.tenant_id == tenant_id)
        .scalar()
        or 0.0
    )
    reconciliation = reconcile_invoice_with_costs(parsed["extracted_total"], float(platform_total), threshold_pct)
    return {
        "tenant_id": tenant_id,
        "invoice": parsed,
        "platform_total": round(float(platform_total), 2),
        "reconciliation": reconciliation,
    }
