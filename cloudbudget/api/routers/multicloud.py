from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.ingestion_service import ingest_cost_records
from api.services.multicloud_service import available_providers, collect_multicloud_costs

router = APIRouter(prefix="/multicloud", tags=["multicloud"])


@router.get("/providers")
async def providers() -> dict:
    return {"providers": available_providers()}


@router.post("/collect")
async def collect(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(get_tenant_id),
    providers: list[str] | None = Query(default=None),
) -> dict:
    try:
        payload = collect_multicloud_costs(tenant_id=tenant_id, providers=providers)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    ingested = ingest_cost_records(db, payload)
    return {"tenant_id": tenant_id, "providers": providers or available_providers(), "ingested": ingested}
