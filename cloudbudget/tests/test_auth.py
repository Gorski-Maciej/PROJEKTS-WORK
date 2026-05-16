import pytest

pytest.importorskip("jose")
pytest.importorskip("passlib")

from api.core.security import hash_password, verify_password


def test_hash_and_verify_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("bad", hashed)
