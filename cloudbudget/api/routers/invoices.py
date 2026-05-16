from fastapi import APIRouter
from pydantic import BaseModel
from api.services.ocr.invoice_service import parse_invoice_text

router = APIRouter(prefix="/invoices", tags=["invoices"])


class InvoiceRequest(BaseModel):
    text: str


@router.post('/parse')
async def parse_invoice(req: InvoiceRequest) -> dict:
    return parse_invoice_text(req.text)
