from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from api.core.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_ctx.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_ctx.verify(password, hashed)


def create_access_token(subject: str, tenant_id: int, expires_minutes: int = 60) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "tenant_id": tenant_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
