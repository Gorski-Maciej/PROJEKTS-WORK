from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import Tenant
from api.services.actions.action_service import execute_action
from api.services.ocr.invoice_service import parse_invoice_text


def test_execute_action_returns_audit():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add(Tenant(id=1, name="tenant1"))
    db.commit()

    result = execute_action(db, 1, "stop_instance", "i-123", "admin")
    assert result["status"] == "executed"
    assert result["audit"]["resource_id"] == "i-123"


def test_parse_invoice_text_extracts_total():
    result = parse_invoice_text("EC2 12.50 Storage 7.25 Support 2.00")
    assert result["line_items_detected"] == 3
    assert result["extracted_total"] == 21.75
