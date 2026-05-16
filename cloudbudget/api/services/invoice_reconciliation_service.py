from __future__ import annotations

from datetime import date, datetime, time, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from api.models.entities import CostRecord
from api.services.ocr.invoice_service import parse_invoice_text
from api.services.reconciliation_service import reconcile_invoice_with_costs


def _period_bounds(start_date: date | None, end_date: date | None) -> tuple[datetime | None, datetime | None]:
    start_dt = datetime.combine(start_date, time.min, tzinfo=timezone.utc) if start_date else None
    end_dt = datetime.combine(end_date, time.max, tzinfo=timezone.utc) if end_date else None
    return start_dt, end_dt


def reconcile_invoice_text(
    db: Session,
    tenant_id: int,
    invoice_text: str,
    threshold_pct: float = 1.0,
    start_date: date | None = None,
    end_date: date | None = None,
) -> dict:
    parsed = parse_invoice_text(invoice_text)

    # if invoice_date was extracted and explicit period not provided, use invoice day.
    if parsed.get("invoice_date") and start_date is None and end_date is None:
        inferred = date.fromisoformat(parsed["invoice_date"])
        start_date = inferred
        end_date = inferred

    start_dt, end_dt = _period_bounds(start_date, end_date)

    query = db.query(func.coalesce(func.sum(CostRecord.amount_usd), 0)).filter(CostRecord.tenant_id == tenant_id)
    if start_dt is not None:
        query = query.filter(CostRecord.collected_at >= start_dt)
    if end_dt is not None:
        query = query.filter(CostRecord.collected_at <= end_dt)

    platform_total = query.scalar() or 0.0
    reconciliation = reconcile_invoice_with_costs(parsed["extracted_total"], float(platform_total), threshold_pct)

    return {
        "tenant_id": tenant_id,
        "invoice": parsed,
        "platform_total": round(float(platform_total), 2),
        "period": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        },
        "reconciliation": reconciliation,
    }
