from pydantic import BaseModel, Field


class IncidentOut(BaseModel):
    id: int
    type: str
    status: str = "open"
    source_mcp: str
    payload: dict = Field(default_factory=dict)
    severity: str = "medium"
    recommended_actions: list[dict] = Field(default_factory=list)


class SummaryOut(BaseModel):
    incidents_open: int
    incidents_acknowledged: int
    agents_online: int
    total_metrics: int
