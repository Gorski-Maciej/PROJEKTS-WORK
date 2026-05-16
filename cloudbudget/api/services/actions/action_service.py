from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from api.models.entities import ActionLog, ActionRequestLog


@dataclass
class ActionAudit:
    tenant_id: int
    action: str
    resource_id: str
    approved_by: str
    executed_at: str


def create_action_request(db: Session, tenant_id: int, action: str, resource_id: str, requested_by: str, reason: str = "") -> dict:
    req = ActionRequestLog(
        tenant_id=tenant_id,
        action=action,
        resource_id=resource_id,
        requested_by=requested_by,
        reason=reason,
        status="pending",
    )
    db.add(req)
    db.commit()
    db.refresh(req)
    return {"request_id": req.id, "status": req.status}


def execute_action(db: Session, tenant_id: int, action: str, resource_id: str, approved_by: str, request_id: int | None = None) -> dict:
    if request_id is not None:
        req = db.query(ActionRequestLog).filter(
            ActionRequestLog.id == request_id,
            ActionRequestLog.tenant_id == tenant_id,
        ).first()
        if req is None:
            return {"status": "error", "detail": "request_not_found"}
        if req.status != "pending":
            return {"status": "error", "detail": "request_not_pending"}
        req.status = "approved"
        req.approved_by = approved_by
        req.decided_at = datetime.now(timezone.utc)

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
    payload = {"status": "executed", "audit": audit.__dict__, "action_log_id": log.id}
    if request_id is not None:
        payload["request_id"] = request_id
    return payload


def list_action_requests(db: Session, tenant_id: int, status: str | None = None) -> list[dict]:
    q = db.query(ActionRequestLog).filter(ActionRequestLog.tenant_id == tenant_id)
    if status:
        q = q.filter(ActionRequestLog.status == status)
    return [
        {
            "id": r.id,
            "action": r.action,
            "resource_id": r.resource_id,
            "requested_by": r.requested_by,
            "reason": r.reason,
            "status": r.status,
        }
        for r in q.order_by(ActionRequestLog.id.desc()).all()
    ]
