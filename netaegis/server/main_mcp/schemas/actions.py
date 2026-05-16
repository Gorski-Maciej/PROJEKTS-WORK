from pydantic import BaseModel, Field


class ActionRequest(BaseModel):
    source_mcp: str
    target: str
    action_type: str
    params: dict = Field(default_factory=dict)


class ActionResult(BaseModel):
    ok: bool
    message: str
