from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(payload: LoginIn):
    if payload.username == 'admin' and payload.password == 'admin':
        return {'access_token': 'dev-token-admin', 'token_type': 'bearer', 'role': 'admin'}
    raise HTTPException(status_code=401, detail='invalid_credentials')


@router.get('/me')
async def me():
    return {'username': 'admin', 'role': 'admin'}
