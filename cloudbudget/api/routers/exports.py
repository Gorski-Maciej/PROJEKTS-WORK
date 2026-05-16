from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse
from api.core.database import get_db
from api.services.export_service import export_costs_csv

router = APIRouter(prefix="/exports", tags=["exports"])


@router.get('/costs/{tenant_id}.csv')
async def export_costs(tenant_id: int, db: Session = Depends(get_db)) -> PlainTextResponse:
    content = export_costs_csv(db, tenant_id)
    return PlainTextResponse(content, media_type="text/csv")
