from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.core.security import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

# demo in-memory identity store
_USERS: dict[str, str] = {}


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post('/register')
async def register(req: RegisterRequest) -> dict:
    if req.username in _USERS:
        raise HTTPException(status_code=409, detail="User exists")
    _USERS[req.username] = hash_password(req.password)
    return {"status": "registered", "username": req.username}


@router.post('/login')
async def login(req: LoginRequest) -> dict:
    hashed = _USERS.get(req.username)
    if not hashed or not verify_password(req.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(req.username)
    return {"access_token": token, "token_type": "bearer"}
