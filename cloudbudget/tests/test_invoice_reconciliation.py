from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import Tenant, CostRecord
from api.services.invoice_reconciliation_service import reconcile_invoice_text


def test_reconcile_invoice_text():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="tenant1"))
    db.add_all([
        CostRecord(tenant_id=1, provider="aws", service="ec2", resource_id="r1", amount_usd=10.5, usage_quantity=1, collected_at=datetime.now(timezone.utc)),
        CostRecord(tenant_id=1, provider="aws", service="s3", resource_id="r2", amount_usd=9.5, usage_quantity=1, collected_at=datetime.now(timezone.utc)),
    ])
    db.commit()

    result = reconcile_invoice_text(db, 1, "line1 12.00 line2 8.00", threshold_pct=5)
    assert result["invoice"]["extracted_total"] == 20.0
    assert result["reconciliation"]["within_threshold"] is True
