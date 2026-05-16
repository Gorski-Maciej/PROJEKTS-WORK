from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from server.operational_mcp.services.action_executor import ActionExecutor

router = APIRouter(prefix="/api/actions", tags=["actions"])


class ActionIn(BaseModel):
    target: str
    action_type: str
    params: dict = Field(default_factory=dict)


@router.post("/execute")
async def execute_action(payload: ActionIn, request: Request):
    executor = ActionExecutor()
    ok = False
    if payload.action_type == "block_ip":
        ip = payload.params.get("ip", "")
        ok = await executor.execute_block_ip(payload.target, ip)
    request.app.state.state.events.append({
        "type": "action_result",
        "payload": {"target": payload.target, "action_type": payload.action_type, "ok": ok},
    })
    return {"ok": ok}
