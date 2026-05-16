from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.actions.action_service import execute_action, create_action_request, list_action_requests

router = APIRouter(prefix="/actions", tags=["actions"])


class ActionRequest(BaseModel):
    action: str
    resource_id: str
    approved_by: str
    request_id: int | None = None


class ActionApprovalRequest(BaseModel):
    action: str
    resource_id: str
    requested_by: str
    reason: str = ""


@router.post('/request')
async def action_request(req: ActionApprovalRequest, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return create_action_request(db, tenant_id, req.action, req.resource_id, req.requested_by, req.reason)


@router.get('/requests')
async def action_requests(status: str | None = Query(default=None), db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return {"items": list_action_requests(db, tenant_id, status=status)}


@router.post('/execute')
async def action_execute(req: ActionRequest, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return execute_action(db, tenant_id, req.action, req.resource_id, req.approved_by, req.request_id)
