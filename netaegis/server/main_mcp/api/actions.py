from fastapi import APIRouter, Request
from server.main_mcp.schemas.actions import ActionRequest

router = APIRouter(prefix="/api/actions", tags=["actions"])


@router.post("/enqueue")
async def enqueue_action(payload: ActionRequest, request: Request):
    queue = request.app.state.action_queue
    action = payload.model_dump()
    action["id"] = len(queue) + 1
    action["status"] = "queued"
    queue.append(action)
    return {"ok": True, "action_id": action["id"]}


@router.get("/")
async def list_actions(request: Request):
    return request.app.state.action_queue
