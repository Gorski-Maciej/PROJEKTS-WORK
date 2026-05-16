import json
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NotificationEvent:
    channel: str
    severity: str
    title: str
    message: str
    created_at: str


def build_notification(channel: str, severity: str, title: str, message: str) -> dict:
    event = NotificationEvent(
        channel=channel,
        severity=severity,
        title=title,
        message=message,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    return event.__dict__


def render_slack_payload(event: dict) -> dict:
    return {
        "text": f"[{event['severity'].upper()}] {event['title']}",
        "attachments": [{"text": event["message"], "footer": f"CloudBudget • {event['created_at']}"}],
    }


def render_webhook_payload(event: dict) -> str:
    return json.dumps(event)
