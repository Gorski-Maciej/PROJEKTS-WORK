import pytest

pytest.importorskip("prometheus_client")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from api.core.database import Base
from api.models.entities import Tenant, Budget, CostRecord
from api.services.budget_service import budget_status


def test_budget_status_has_forecast_state():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="t1"))
    db.add(Budget(tenant_id=1, monthly_budget_usd=100))
    db.add(CostRecord(tenant_id=1, provider="aws", service="ec2", resource_id="i-1", amount_usd=95, usage_quantity=1, collected_at=datetime.utcnow()))
    db.commit()

    status = budget_status(db, 1)
    assert status["forecast_state"] == "at_risk"
