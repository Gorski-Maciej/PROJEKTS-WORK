from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import ActionLog, ActionRequestLog, Tenant
from api.services.actions.action_service import execute_action, create_action_request, list_action_requests


def _session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="t1"))
    db.commit()
    return db


def test_execute_action_persists_log():
    db = _session()
    result = execute_action(db, tenant_id=1, action="stop_instance", resource_id="i-1", approved_by="admin")
    assert result["status"] == "executed"
    assert result["action_log_id"] > 0
    assert db.query(ActionLog).count() == 1


def test_request_then_execute_updates_request_status():
    db = _session()
    req = create_action_request(db, tenant_id=1, action="stop_instance", resource_id="i-1", requested_by="ops", reason="idle")
    result = execute_action(
        db,
        tenant_id=1,
        action="stop_instance",
        resource_id="i-1",
        approved_by="admin",
        request_id=req["request_id"],
    )
    assert result["status"] == "executed"
    assert db.query(ActionRequestLog).first().status == "approved"


def test_list_action_requests_by_status():
    db = _session()
    create_action_request(db, tenant_id=1, action="stop_instance", resource_id="i-2", requested_by="ops")
    pending = list_action_requests(db, tenant_id=1, status="pending")
    assert len(pending) == 1
