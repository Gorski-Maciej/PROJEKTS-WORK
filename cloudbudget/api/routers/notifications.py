from fastapi import APIRouter
from pydantic import BaseModel, Field
from api.services.notification_service import build_notification, render_slack_payload, render_webhook_payload

router = APIRouter(prefix="/notifications", tags=["notifications"])


class NotificationRequest(BaseModel):
    channel: str = Field(pattern="^(slack|webhook|email)$")
    severity: str = Field(default="info")
    title: str
    message: str


@router.post('/preview')
async def preview(req: NotificationRequest) -> dict:
    event = build_notification(req.channel, req.severity, req.title, req.message)
    if req.channel == "slack":
        return {"event": event, "payload": render_slack_payload(event)}
    if req.channel == "webhook":
        return {"event": event, "payload": render_webhook_payload(event)}
    return {"event": event, "payload": {"subject": req.title, "body": req.message}}
