from __future__ import annotations

from datetime import datetime, timezone


class OperationalState:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self.agents: dict[str, dict] = {}

    def touch_agent(self, agent_id: str) -> None:
        self.agents[agent_id] = {"status": "online", "last_seen": datetime.now(timezone.utc).isoformat()}
