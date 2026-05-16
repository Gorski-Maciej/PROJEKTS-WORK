from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.schemas.common import CostRecordIn
from api.services.ingestion_service import ingest_cost_records
from api.services.analytics_service import cost_summary

router = APIRouter(prefix="/costs", tags=["costs"])


@router.post("/ingest")
async def ingest(payload: list[CostRecordIn], db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    if any(p.tenant_id != tenant_id for p in payload):
        raise HTTPException(status_code=400, detail="Payload tenant_id must match X-Tenant-ID")
    count = ingest_cost_records(db, payload)
    return {"ingested": count}


@router.get("/summary")
async def summary(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return cost_summary(db, tenant_id)
