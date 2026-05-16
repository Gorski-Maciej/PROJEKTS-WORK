from api.services.ocr.invoice_service import parse_invoice_text


def test_parse_invoice_with_metadata():
    text = """Invoice No: INV-2026-001\nDate: 16/05/2026\nVendor: Example Cloud\nCompute 12.50\nStorage 7,50"""
    result = parse_invoice_text(text)
    assert result["invoice_number"] == "INV-2026-001"
    assert result["invoice_date"] == "2026-05-16"
    assert result["vendor"] == "Example Cloud"
    assert result["extracted_total"] == 20.0
    assert result["line_items_detected"] == 2
