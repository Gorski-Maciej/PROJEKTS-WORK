from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.services.ri_optimizer_service import recommend_ri_plan
from api.services.simulation_service import run_provider_migration_simulation

router = APIRouter(prefix="/optimizations", tags=["optimizations"])


class RIRequest(BaseModel):
    monthly_on_demand_cost: float = Field(gt=0)
    commitment_years: int = Field(default=1)


class MigrationRequest(BaseModel):
    instance_count: int = Field(gt=0)
    current_unit_cost: float = Field(gt=0)
    target_unit_cost: float = Field(gt=0)


@router.post('/ri')
async def ri(req: RIRequest) -> dict:
    return recommend_ri_plan(req.monthly_on_demand_cost, req.commitment_years)


@router.post('/migration')
async def migration(req: MigrationRequest) -> dict:
    return run_provider_migration_simulation(req.instance_count, req.current_unit_cost, req.target_unit_cost)
