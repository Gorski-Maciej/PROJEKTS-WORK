from api.services.multicloud_service import available_providers, collect_multicloud_costs


def test_available_providers():
    providers = available_providers()
    assert "aws" in providers
    assert "azure" in providers


def test_collect_all_providers():
    rows = collect_multicloud_costs(tenant_id=5)
    assert len(rows) >= 10
    assert all(r.tenant_id == 5 for r in rows)


def test_collect_invalid_provider():
    try:
        collect_multicloud_costs(tenant_id=1, providers=["invalid"])
        assert False
    except ValueError as exc:
        assert "Unsupported provider" in str(exc)
