import pytest

pytest.importorskip("jose")

from fastapi import HTTPException

from api.core.security import create_access_token
from api.core.tenant import get_tenant_id


def test_get_tenant_id_without_token_works_for_header_only():
    assert get_tenant_id(x_tenant_id="2", authorization=None) == 2


def test_get_tenant_id_with_matching_token_tenant():
    token = create_access_token("alice", tenant_id=7)
    assert get_tenant_id(x_tenant_id="7", authorization=f"Bearer {token}") == 7


def test_get_tenant_id_with_mismatched_token_tenant():
    token = create_access_token("alice", tenant_id=7)
    with pytest.raises(HTTPException) as exc:
        get_tenant_id(x_tenant_id="8", authorization=f"Bearer {token}")
    assert exc.value.status_code == 403
