from api.services.budget_service import budget_status
from sqlalchemy.orm import Session


def evaluate_budget_alert(db: Session, tenant_id: int) -> dict:
    status = budget_status(db, tenant_id)
    state = status.get("state", "ok")
    severity = "info"
    if state in {"warning", "exceeded", "critical"}:
        severity = "critical" if state == "critical" else "warning"
    return {"tenant_id": tenant_id, "state": state, "severity": severity, "payload": status}
