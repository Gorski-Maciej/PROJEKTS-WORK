from __future__ import annotations

from typing import Any


class MainStore:
    def __init__(self) -> None:
        self.incidents: list[dict[str, Any]] = []
        self.metrics: list[dict[str, Any]] = []
        self.agents: dict[str, dict[str, Any]] = {}

    def add_incident(self, payload: dict[str, Any]) -> dict[str, Any]:
        payload = dict(payload)
        payload["id"] = len(self.incidents) + 1
        self.incidents.append(payload)
        return payload

    def acknowledge(self, incident_id: int) -> bool:
        for incident in self.incidents:
            if incident["id"] == incident_id:
                incident["status"] = "acknowledged"
                return True
        return False
