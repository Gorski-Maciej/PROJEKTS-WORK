from fastapi import APIRouter
from pydantic import BaseModel
from api.services.dlq_service import dlq_store

router = APIRouter(prefix="/dlq", tags=["dlq"])


class DLQAddRequest(BaseModel):
    message_id: str
    queue: str
    payload: dict
    reason: str


class DLQRequeueRequest(BaseModel):
    message_id: str


@router.get('')
async def list_dlq() -> list[dict]:
    return dlq_store.list()


@router.post('')
async def add_dlq(req: DLQAddRequest) -> dict:
    return dlq_store.add(req.message_id, req.queue, req.payload, req.reason).__dict__


@router.post('/requeue')
async def requeue(req: DLQRequeueRequest) -> dict:
    return dlq_store.requeue(req.message_id)
