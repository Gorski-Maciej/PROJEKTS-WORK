from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import ActionLog, Tenant
from api.services.actions.action_service import execute_action


def test_execute_action_persists_log():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="t1"))
    db.commit()

    result = execute_action(db, tenant_id=1, action="stop_instance", resource_id="i-1", approved_by="admin")
    assert result["status"] == "executed"
    assert result["action_log_id"] > 0

    count = db.query(ActionLog).count()
    assert count == 1
