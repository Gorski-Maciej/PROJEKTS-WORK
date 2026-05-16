from api.services.reconciliation_service import reconcile_invoice_with_costs


def test_reconciliation_threshold():
    res = reconcile_invoice_with_costs(101, 100, threshold_pct=2)
    assert res["within_threshold"] is True


def test_reconciliation_outside_threshold():
    res = reconcile_invoice_with_costs(130, 100, threshold_pct=5)
    assert res["within_threshold"] is False
