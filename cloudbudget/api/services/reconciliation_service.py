def reconcile_invoice_with_costs(invoice_total: float, platform_total: float, threshold_pct: float = 1.0) -> dict:
    if platform_total == 0:
        delta_pct = 100.0 if invoice_total != 0 else 0.0
    else:
        delta_pct = abs(invoice_total - platform_total) / platform_total * 100
    diff = invoice_total - platform_total
    return {
        "invoice_total": round(invoice_total, 2),
        "platform_total": round(platform_total, 2),
        "difference": round(diff, 2),
        "delta_pct": round(delta_pct, 2),
        "within_threshold": delta_pct <= threshold_pct,
    }
