from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.services.whatif_service import simulate_cloud_migration, simulate_rightsizing

router = APIRouter(prefix="/whatif", tags=["whatif"])


class MigrationScenario(BaseModel):
    current_monthly_cost: float = Field(gt=0)
    target_discount_pct: float = Field(ge=0, le=100)
    one_time_migration_cost: float = Field(default=0, ge=0)


class RightsizingScenario(BaseModel):
    current_instance_cost: float = Field(gt=0)
    utilization_pct: float = Field(ge=0, le=100)


@router.post('/migration')
async def migration(req: MigrationScenario) -> dict:
    return simulate_cloud_migration(req.current_monthly_cost, req.target_discount_pct, req.one_time_migration_cost)


@router.post('/rightsizing')
async def rightsizing(req: RightsizingScenario) -> dict:
    return simulate_rightsizing(req.current_instance_cost, req.utilization_pct)
