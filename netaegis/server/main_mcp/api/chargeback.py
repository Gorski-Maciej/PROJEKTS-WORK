from fastapi import APIRouter

router = APIRouter(prefix="/api/chargeback", tags=["chargeback"])


@router.get("/summary")
async def summary():
    return {
        "currency": "USD",
        "period": "monthly",
        "items": [
            {"tenant": "security", "cost": 120.0},
            {"tenant": "platform", "cost": 95.0},
        ],
    }
