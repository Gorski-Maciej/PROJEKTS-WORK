from fastapi import APIRouter, Request
from server.main_mcp.schemas.events import SyncIn

router = APIRouter(prefix="/api/op", tags=["sync"])


@router.post("/sync")
async def sync(payload: SyncIn, request: Request):
    store = request.app.state.store
    processor = request.app.state.processor

    for event in payload.events:
        incident = processor.event_to_incident(payload.source_mcp, event.model_dump())
        store.add_incident(incident)

    return {"ok": True, "count": len(payload.events)}
