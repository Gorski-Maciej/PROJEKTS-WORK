from fastapi import APIRouter, Request
from server.operational_mcp.services.sync_service import SyncService

router = APIRouter(prefix="/api", tags=["sync"])


@router.get("/buffer")
async def buffer_state(request: Request):
    state = request.app.state.state
    return {"events_buffered": len(state.events), "agents": len(state.agents)}


@router.post("/sync")
async def sync_to_main(request: Request):
    state = request.app.state.state
    if not state.events:
        return {"ok": True, "count": 0}

    service = SyncService(request.app.state.main_mcp_url)
    events = list(state.events)
    resp = await service.sync(request.app.state.node_id, events)
    if resp.status_code == 200:
        state.events.clear()
        return {"ok": True, "count": len(events), "mode": "online"}
    return {"ok": False, "status_code": resp.status_code, "mode": "autonomous"}
