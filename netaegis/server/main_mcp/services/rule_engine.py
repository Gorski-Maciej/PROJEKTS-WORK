class RuleEngine:
    def evaluate(self, event_type: str, payload: dict) -> list[dict]:
        actions: list[dict] = []
        if event_type == "failed_login" and payload.get("count", 0) >= 5:
            actions.append({"action_type": "block_ip", "params": {"ip": payload.get("ip")}})
        if event_type == "http_5xx" and int(payload.get("status", 200)) >= 500:
            actions.append({"action_type": "create_incident", "params": payload})
        return actions
