from fastapi import APIRouter, Request
from server.main_mcp.schemas.incidents import IncidentOut

router = APIRouter(prefix="/api/incidents", tags=["incidents"])


@router.get("/", response_model=list[IncidentOut])
async def list_incidents(request: Request):
    return request.app.state.store.incidents


@router.post("/{incident_id}/acknowledge")
async def acknowledge(incident_id: int, request: Request):
    ok = request.app.state.store.acknowledge(incident_id)
    return {"ok": ok}
