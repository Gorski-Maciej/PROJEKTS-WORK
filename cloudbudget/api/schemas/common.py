from pydantic import BaseModel, Field
from datetime import datetime


class CostRecordIn(BaseModel):
    tenant_id: int
    provider: str
    service: str
    resource_id: str
    amount_usd: float = Field(ge=0)
    usage_quantity: float = Field(default=0, ge=0)
    collected_at: datetime


class RecommendationOut(BaseModel):
    category: str
    resource_id: str
    estimated_savings_usd: float
    confidence: float


class SimulationRequest(BaseModel):
    tenant_id: int
    scenario: str
    provider_from: str | None = None
    provider_to: str | None = None
    count: int = Field(default=1, ge=1)
    resize_factor: float = Field(default=1.0, gt=0)


class BudgetRequest(BaseModel):
    tenant_id: int
    monthly_budget_usd: float = Field(gt=0)
