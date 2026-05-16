import pytest

pytest.importorskip("jose")
pytest.importorskip("passlib")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.core.database import Base
from api.core.security import hash_password, verify_password, create_access_token, decode_access_token
from api.models.entities import Tenant, User, UserTenant


def test_hash_and_verify_password():
    hashed = hash_password("secret123")
    assert verify_password("secret123", hashed)
    assert not verify_password("bad", hashed)


def test_token_contains_tenant_claim():
    token = create_access_token("alice", tenant_id=7)
    payload = decode_access_token(token)
    assert payload["sub"] == "alice"
    assert payload["tenant_id"] == 7


def test_user_tenant_membership_model():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    tenant = Tenant(name="demo")
    db.add(tenant)
    db.flush()
    user = User(username="john", password_hash=hash_password("supersecret"), is_active=True)
    db.add(user)
    db.flush()
    db.add(UserTenant(user_id=user.id, tenant_id=tenant.id, role="admin"))
    db.commit()

    assert db.query(UserTenant).count() == 1
