from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/policies", tags=["policies"])


class PolicyIn(BaseModel):
    name: str
    enabled: bool = True
    conditions: dict = Field(default_factory=dict)
    actions: list[dict] = Field(default_factory=list)


@router.get("/")
async def list_policies(request: Request):
    return request.app.state.policies


@router.post("/")
async def create_policy(payload: PolicyIn, request: Request):
    policy = payload.model_dump()
    policy["id"] = len(request.app.state.policies) + 1
    request.app.state.policies.append(policy)
    return {"ok": True, "policy": policy}
