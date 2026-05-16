from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import Tenant, CostRecord
from api.services.chargeback_service import showback_by_provider, chargeback_by_service


def test_chargeback_aggregations():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="tenant1"))
    db.add_all([
        CostRecord(tenant_id=1, provider="aws", service="ec2", resource_id="r1", amount_usd=10, usage_quantity=1, collected_at=datetime.now(timezone.utc)),
        CostRecord(tenant_id=1, provider="aws", service="s3", resource_id="r2", amount_usd=5, usage_quantity=1, collected_at=datetime.now(timezone.utc)),
        CostRecord(tenant_id=1, provider="gcp", service="gce", resource_id="r3", amount_usd=8, usage_quantity=1, collected_at=datetime.now(timezone.utc)),
    ])
    db.commit()

    by_provider = showback_by_provider(db, 1)
    by_service = chargeback_by_service(db, 1)
    assert any(r["provider"] == "aws" and r["amount_usd"] == 15.0 for r in by_provider)
    assert any(r["service"] == "ec2" and r["amount_usd"] == 10.0 for r in by_service)
