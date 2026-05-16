from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from api.models.entities import ActionLog


@dataclass
class ActionAudit:
    tenant_id: int
    action: str
    resource_id: str
    approved_by: str
    executed_at: str


def execute_action(db: Session, tenant_id: int, action: str, resource_id: str, approved_by: str) -> dict:
    executed_at = datetime.now(timezone.utc)
    log = ActionLog(
        tenant_id=tenant_id,
        action=action,
        resource_id=resource_id,
        approved_by=approved_by,
        executed_at=executed_at,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    audit = ActionAudit(
        tenant_id=tenant_id,
        action=action,
        resource_id=resource_id,
        approved_by=approved_by,
        executed_at=executed_at.isoformat(),
    )
    return {"status": "executed", "audit": audit.__dict__, "action_log_id": log.id}
