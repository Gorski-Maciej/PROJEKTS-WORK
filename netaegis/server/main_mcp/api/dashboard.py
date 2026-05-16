from fastapi import APIRouter, Request
from server.main_mcp.schemas.incidents import SummaryOut

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=SummaryOut)
async def summary(request: Request):
    store = request.app.state.store
    incidents = store.incidents
    return SummaryOut(
        incidents_open=len([i for i in incidents if i["status"] == "open"]),
        incidents_acknowledged=len([i for i in incidents if i["status"] == "acknowledged"]),
        agents_online=len(store.agents),
        total_metrics=len(store.metrics),
    )
