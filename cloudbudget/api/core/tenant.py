from fastapi import Header, HTTPException


def get_tenant_id(x_tenant_id: str = Header(..., alias="X-Tenant-ID")) -> int:
    try:
        tenant_id = int(x_tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="X-Tenant-ID must be integer") from exc
    if tenant_id <= 0:
        raise HTTPException(status_code=400, detail="X-Tenant-ID must be positive")
    return tenant_id
