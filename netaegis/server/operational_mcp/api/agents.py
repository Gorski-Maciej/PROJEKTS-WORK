from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/agents", tags=["agents"])


class AgentMetric(BaseModel):
    agent_id: str
    name: str
    value: float


class AgentLog(BaseModel):
    agent_id: str
    type: str
    details: dict = Field(default_factory=dict)


class Heartbeat(BaseModel):
    agent_id: str
    name: str | None = None


@router.post("/metrics")
async def metric(metric: AgentMetric, request: Request):
    state = request.app.state.state
    state.events.append(
        {"type": "metric", "payload": {"agent_id": metric.agent_id, "name": metric.name, "value": metric.value}}
    )
    state.touch_agent(metric.agent_id)
    return {"ok": True}


@router.post("/logs")
async def log(payload: AgentLog, request: Request):
    state = request.app.state.state
    state.events.append({"type": payload.type, "payload": {"agent_id": payload.agent_id, **payload.details}})
    state.touch_agent(payload.agent_id)
    return {"ok": True}


@router.post("/heartbeat")
async def heartbeat(payload: Heartbeat, request: Request):
    state = request.app.state.state
    state.touch_agent(payload.agent_id)
    return {"ok": True, "agent": payload.agent_id}


@router.get("/")
async def agents(request: Request):
    return request.app.state.state.agents
