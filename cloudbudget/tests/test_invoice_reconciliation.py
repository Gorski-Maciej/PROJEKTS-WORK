from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.core.database import Base
from api.models.entities import CostRecord, Tenant
from api.services.invoice_reconciliation_service import reconcile_invoice_text


def test_reconcile_invoice_text():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="tenant1"))
    db.add_all([
        CostRecord(tenant_id=1, provider="aws", service="ec2", resource_id="r1", amount_usd=10.5, usage_quantity=1, collected_at=datetime(2026, 5, 16, 10, 0, tzinfo=timezone.utc)),
        CostRecord(tenant_id=1, provider="aws", service="s3", resource_id="r2", amount_usd=9.5, usage_quantity=1, collected_at=datetime(2026, 5, 16, 16, 0, tzinfo=timezone.utc)),
        CostRecord(tenant_id=1, provider="aws", service="rds", resource_id="r3", amount_usd=50.0, usage_quantity=1, collected_at=datetime(2026, 5, 17, 16, 0, tzinfo=timezone.utc)),
    ])
    db.commit()

    result = reconcile_invoice_text(db, 1, "Invoice No: INV-1 Date: 2026-05-16 line1 12.00 line2 8.00", threshold_pct=5)
    assert result["invoice"]["extracted_total"] == 20.0
    assert result["reconciliation"]["within_threshold"] is True
    assert result["platform_total"] == 20.0
    assert result["period"]["start_date"] == "2026-05-16"


def test_reconcile_invoice_text_with_manual_period():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=2, name="tenant2"))
    db.add_all([
        CostRecord(tenant_id=2, provider="aws", service="ec2", resource_id="a", amount_usd=5.0, usage_quantity=1, collected_at=datetime(2026, 5, 1, 10, 0, tzinfo=timezone.utc)),
        CostRecord(tenant_id=2, provider="aws", service="ec2", resource_id="b", amount_usd=7.0, usage_quantity=1, collected_at=datetime(2026, 5, 2, 10, 0, tzinfo=timezone.utc)),
        CostRecord(tenant_id=2, provider="aws", service="ec2", resource_id="c", amount_usd=20.0, usage_quantity=1, collected_at=datetime(2026, 5, 8, 10, 0, tzinfo=timezone.utc)),
    ])
    db.commit()

    result = reconcile_invoice_text(
        db,
        2,
        "line 12.00",
        threshold_pct=0,
        start_date=datetime(2026, 5, 1, tzinfo=timezone.utc).date(),
        end_date=datetime(2026, 5, 2, tzinfo=timezone.utc).date(),
    )
    assert result["platform_total"] == 12.0
    assert result["reconciliation"]["difference"] == 0.0
