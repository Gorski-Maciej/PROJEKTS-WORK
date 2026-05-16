from fastapi import APIRouter
from api.schemas.common import SimulationRequest
from api.services.simulation_service import run_what_if_simulation

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post("/what-if")
async def what_if(req: SimulationRequest) -> dict:
    base = 10000.0 * req.count
    discount = 0.15 if req.provider_from and req.provider_to and req.provider_from != req.provider_to else 0.0
    return run_what_if_simulation(base, req.resize_factor, discount)
