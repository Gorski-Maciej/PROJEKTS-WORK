from pydantic import BaseModel, Field

class EventIn(BaseModel):
    type: str = Field(default="event")
    payload: dict = Field(default_factory=dict)

class SyncIn(BaseModel):
    source_mcp: str
    events: list[EventIn]
