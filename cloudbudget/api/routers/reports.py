from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import PlainTextResponse
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.reporting_service import build_finops_report

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get('/finops')
async def finops_report(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> dict:
    return build_finops_report(db, tenant_id)


@router.get('/finops.txt')
async def finops_report_txt(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> PlainTextResponse:
    report = build_finops_report(db, tenant_id)
    return PlainTextResponse(report["report_text"], media_type="text/plain")
