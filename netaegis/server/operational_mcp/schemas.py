from pydantic import BaseModel, Field


class SyncPayload(BaseModel):
    source_mcp: str
    events: list[dict] = Field(default_factory=list)
