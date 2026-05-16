from __future__ import annotations

import re
from datetime import date

AMOUNT_RE = re.compile(r"\b\d+[\.,]\d{2}\b")
INVOICE_NO_RE = re.compile(r"(?:invoice|faktura)\s*(?:no|nr|#)?\s*[:\-]?\s*([A-Z0-9\-/]+)", re.IGNORECASE)
DATE_RE = re.compile(r"\b(\d{4}-\d{2}-\d{2}|\d{2}[./-]\d{2}[./-]\d{4})\b")
VENDOR_RE = re.compile(r"(?:vendor|seller|sprzedawca)\s*[:\-]\s*([^\n]+)", re.IGNORECASE)


def _parse_date(raw: str) -> str | None:
    if not raw:
        return None
    if "-" in raw and len(raw.split("-")) == 3 and len(raw.split("-")[0]) == 4:
        return raw
    for sep in (".", "/", "-"):
        if sep in raw:
            dd, mm, yyyy = raw.split(sep)
            try:
                return date(int(yyyy), int(mm), int(dd)).isoformat()
            except ValueError:
                return None
    return None


def parse_invoice_text(raw_text: str) -> dict:
    normalized = raw_text.replace(",", ".")
    amounts = [float(x) for x in AMOUNT_RE.findall(normalized)]

    invoice_no = None
    m = INVOICE_NO_RE.search(raw_text)
    if m:
        invoice_no = m.group(1)

    vendor = None
    vm = VENDOR_RE.search(raw_text)
    if vm:
        vendor = vm.group(1).strip()

    date_raw = None
    dm = DATE_RE.search(raw_text)
    if dm:
        date_raw = dm.group(1)

    return {
        "line_items_detected": len(amounts),
        "amounts": amounts,
        "extracted_total": round(sum(amounts), 2),
        "invoice_number": invoice_no,
        "invoice_date": _parse_date(date_raw) if date_raw else None,
        "vendor": vendor,
    }
