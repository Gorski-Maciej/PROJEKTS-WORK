from fastapi import APIRouter, Request
from server.main_mcp.services.prediction import PredictionService

router = APIRouter(prefix="/api/predictions", tags=["predictions"])


@router.get("/incidents")
async def incident_predictions(request: Request):
    service = PredictionService()
    incident_count = len(request.app.state.store.incidents)
    history = [max(0, incident_count - 3), max(0, incident_count - 2), max(0, incident_count - 1), incident_count]
    return service.forecast_incident_pressure(history)
