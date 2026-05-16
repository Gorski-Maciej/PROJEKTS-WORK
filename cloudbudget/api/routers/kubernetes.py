from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.services.kubernetes_cost_service import estimate_k8s_namespace_costs

router = APIRouter(prefix="/kubernetes", tags=["kubernetes"])


class NamespaceUsage(BaseModel):
    namespace: str
    cpu_core_hours: float = Field(ge=0)
    memory_gb_hours: float = Field(ge=0)


class KubernetesCostRequest(BaseModel):
    usage: list[NamespaceUsage]


@router.post('/namespace-costs')
async def namespace_costs(req: KubernetesCostRequest) -> list[dict]:
    return estimate_k8s_namespace_costs([u.model_dump() for u in req.usage])
