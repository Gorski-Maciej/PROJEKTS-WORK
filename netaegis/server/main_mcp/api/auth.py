import os

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

DEMO_USERNAME = os.getenv("NETAEGIS_DEMO_USERNAME")
DEMO_PASSWORD = os.getenv("NETAEGIS_DEMO_PASSWORD")

if not DEMO_USERNAME or not DEMO_PASSWORD:
    raise RuntimeError("NETAEGIS_DEMO_USERNAME and NETAEGIS_DEMO_PASSWORD are required")
if len(DEMO_PASSWORD) < 12:
    raise RuntimeError("NETAEGIS_DEMO_PASSWORD must be at least 12 characters")


class LoginIn(BaseModel):
    username: str
    password: str


@router.post('/login')
async def login(payload: LoginIn):
    if payload.username == DEMO_USERNAME and payload.password == DEMO_PASSWORD:
        return {'access_token': 'dev-token-admin', 'token_type': 'bearer', 'role': 'admin'}
    raise HTTPException(status_code=401, detail='invalid_credentials')


@router.get('/me')
async def me():
    return {'username': DEMO_USERNAME, 'role': 'admin'}
