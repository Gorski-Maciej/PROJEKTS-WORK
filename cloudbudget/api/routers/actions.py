from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.actions.action_service import execute_action

router = APIRouter(prefix="/actions", tags=["actions"])


class ActionRequest(BaseModel):
    action: str
    resource_id: str
    approved_by: str


@router.post('/execute')
async def action_execute(req: ActionRequest, db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return execute_action(db, tenant_id, req.action, req.resource_id, req.approved_by)
