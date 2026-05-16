from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.core.database import get_db
from api.core.tenant import get_tenant_id
from api.services.chargeback_service import showback_by_provider, chargeback_by_service

router = APIRouter(prefix="/chargeback", tags=["chargeback"])


@router.get('/providers')
async def providers(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> list[dict]:
    return showback_by_provider(db, tenant_id)


@router.get('/services')
async def services(db: Session = Depends(get_db), tenant_id: int = Depends(get_tenant_id)) -> list[dict]:
    return chargeback_by_service(db, tenant_id)
