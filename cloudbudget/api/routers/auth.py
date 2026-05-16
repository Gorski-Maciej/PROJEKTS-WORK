from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from api.core.database import get_db
from api.core.security import create_access_token, hash_password, verify_password
from api.models.entities import Tenant, User, UserTenant

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    tenant_name: str = Field(min_length=2)


class LoginRequest(BaseModel):
    username: str
    password: str
    tenant_id: int


@router.post('/register')
async def register(req: RegisterRequest, db: Session = Depends(get_db)) -> dict:
    if db.query(User).filter(User.username == req.username).first():
        raise HTTPException(status_code=409, detail="User exists")

    tenant = db.query(Tenant).filter(Tenant.name == req.tenant_name).first()
    if tenant is None:
        tenant = Tenant(name=req.tenant_name)
        db.add(tenant)
        db.flush()

    user = User(username=req.username, password_hash=hash_password(req.password), is_active=True)
    db.add(user)
    db.flush()

    db.add(UserTenant(user_id=user.id, tenant_id=tenant.id, role="admin"))
    db.commit()
    return {"status": "registered", "username": req.username, "tenant_id": tenant.id}


@router.post('/login')
async def login(req: LoginRequest, db: Session = Depends(get_db)) -> dict:
    user = db.query(User).filter(User.username == req.username, User.is_active == True).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    membership = db.query(UserTenant).filter(UserTenant.user_id == user.id, UserTenant.tenant_id == req.tenant_id).first()
    if membership is None:
        raise HTTPException(status_code=403, detail="Tenant access denied")

    token = create_access_token(req.username, tenant_id=req.tenant_id)
    return {"access_token": token, "token_type": "bearer", "tenant_id": req.tenant_id, "role": membership.role}
