from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/status", tags=["status"])


@router.get("/")
async def status(request: Request):
    state = request.app.state.state
    return {
        "node_id": request.app.state.node_id,
        "agents_online": len(state.agents),
        "events_buffered": len(state.events),
    }
