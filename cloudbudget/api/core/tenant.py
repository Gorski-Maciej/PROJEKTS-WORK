from __future__ import annotations

from fastapi import Header, HTTPException

from api.core.security import decode_access_token


def _parse_bearer_token(authorization: str | None) -> str | None:
    if authorization is None:
        return None
    parts = authorization.strip().split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    return parts[1]


def get_tenant_id(
    x_tenant_id: str = Header(..., alias="X-Tenant-ID"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> int:
    try:
        tenant_id = int(x_tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="X-Tenant-ID must be integer") from exc
    if tenant_id <= 0:
        raise HTTPException(status_code=400, detail="X-Tenant-ID must be positive")

    token = _parse_bearer_token(authorization)
    if token:
        try:
            claims = decode_access_token(token)
        except Exception as exc:
            raise HTTPException(status_code=401, detail="Invalid access token") from exc

        token_tenant = claims.get("tenant_id")
        if token_tenant is None:
            raise HTTPException(status_code=401, detail="Token missing tenant_id claim")
        if int(token_tenant) != tenant_id:
            raise HTTPException(status_code=403, detail="Token tenant_id does not match X-Tenant-ID")

    return tenant_id
