import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("JWT_SECRET")
if not SECRET_KEY:
    raise RuntimeError("JWT_SECRET is required")
if len(SECRET_KEY) < 32:
    raise RuntimeError("JWT_SECRET must be at least 32 characters")

ALGO = "HS256"
oauth2 = OAuth2PasswordBearer(tokenUrl="/token")
ADMIN_PASSWORD = os.getenv("INFRAFLOW_ADMIN_PASSWORD")
VIEWER_PASSWORD = os.getenv("INFRAFLOW_VIEWER_PASSWORD")
if not ADMIN_PASSWORD or not VIEWER_PASSWORD:
    raise RuntimeError("INFRAFLOW_ADMIN_PASSWORD and INFRAFLOW_VIEWER_PASSWORD are required")

USERS = {
    "admin": {"password": ADMIN_PASSWORD, "role": "admin"},
    "viewer": {"password": VIEWER_PASSWORD, "role": "readonly"},
}


def create_access_token(data, expires_delta=None):
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=2))
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGO)


async def verify_token(token: str = Depends(oauth2)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
