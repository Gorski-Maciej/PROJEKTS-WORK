from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/realtime", tags=["realtime"])


@router.get("/health")
async def health(request: Request):
    return {
        "main_mcp": "ok",
        "incidents": len(request.app.state.store.incidents),
        "queued_actions": len(request.app.state.action_queue),
    }
