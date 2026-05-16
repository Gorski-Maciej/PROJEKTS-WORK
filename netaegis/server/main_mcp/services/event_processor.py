from server.main_mcp.services.rule_engine import RuleEngine


class EventProcessor:
    def __init__(self) -> None:
        self.rule_engine = RuleEngine()

    def event_to_incident(self, source_mcp: str, event: dict) -> dict:
        event_type = event.get("type", "event")
        payload = event.get("payload", {})
        actions = self.rule_engine.evaluate(event_type, payload)
        severity = "high" if any(a.get("action_type") == "block_ip" for a in actions) else "medium"
        return {
            "type": event_type,
            "status": "open",
            "source_mcp": source_mcp,
            "payload": payload,
            "recommended_actions": actions,
            "severity": severity,
        }
