import re


def parse_invoice_text(raw_text: str) -> dict:
    amounts = [float(x) for x in re.findall(r"\b\d+\.\d{2}\b", raw_text)]
    total = sum(amounts)
    return {"line_items_detected": len(amounts), "extracted_total": round(total, 2)}
