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

ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

ADMIN_PASSWORD = os.getenv("NETGUARDIAN_ADMIN_PASSWORD")
VIEWER_PASSWORD = os.getenv("NETGUARDIAN_VIEWER_PASSWORD")
if not ADMIN_PASSWORD or not VIEWER_PASSWORD:
    raise RuntimeError("NETGUARDIAN_ADMIN_PASSWORD and NETGUARDIAN_VIEWER_PASSWORD are required")

USERS = {
    "admin": {"password": ADMIN_PASSWORD, "role": "admin"},
    "viewer": {"password": VIEWER_PASSWORD, "role": "readonly"},
}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in USERS:
            raise HTTPException(status_code=401)
        return {"username": username, "role": USERS[username]["role"]}
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token expired") from exc
    except jwt.InvalidTokenError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc


def require_role(role: str):
    async def role_checker(user=Depends(get_current_user)):
        if role == "admin" and user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return role_checker
