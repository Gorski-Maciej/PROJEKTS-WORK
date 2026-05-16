import pytest

pytest.importorskip("prometheus_client")

from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import Tenant, Budget, CostRecord
from api.services.reporting_service import build_finops_report


def test_build_finops_report_contains_sections():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="tenant1"))
    db.add(Budget(tenant_id=1, monthly_budget_usd=100))
    db.add(CostRecord(tenant_id=1, provider="aws", service="ec2", resource_id="r1", amount_usd=20, usage_quantity=1, collected_at=datetime.now(timezone.utc)))
    db.commit()

    report = build_finops_report(db, 1)
    assert "summary" in report
    assert "budget" in report
    assert "forecast" in report
    assert "CloudBudget FinOps Report" in report["report_text"]
