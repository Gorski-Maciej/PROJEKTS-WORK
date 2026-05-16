from fastapi import APIRouter, Request

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


@router.get("/")
async def recommendations(request: Request):
    incidents = request.app.state.store.incidents
    recs = []
    for inc in incidents[-50:]:
        if inc.get("type") == "failed_login":
            recs.append({"incident_id": inc["id"], "priority": "high", "recommendation": "Wymuś MFA i zablokuj adres IP."})
        elif inc.get("type") == "http_5xx":
            recs.append({"incident_id": inc["id"], "priority": "medium", "recommendation": "Sprawdź healthcheck usługi i restart deploymentu."})
    return recs
