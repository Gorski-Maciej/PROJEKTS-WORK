import csv
import io
from sqlalchemy.orm import Session
from api.models.entities import CostRecord


def export_costs_csv(db: Session, tenant_id: int) -> str:
    rows = db.query(CostRecord).filter(CostRecord.tenant_id == tenant_id).all()
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["tenant_id", "provider", "service", "resource_id", "amount_usd", "usage_quantity", "collected_at"])
    for r in rows:
        writer.writerow([r.tenant_id, r.provider, r.service, r.resource_id, r.amount_usd, r.usage_quantity, r.collected_at.isoformat()])
    return buf.getvalue()
