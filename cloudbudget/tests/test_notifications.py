from api.services.notification_service import build_notification, render_slack_payload


def test_notification_payload_shapes():
    event = build_notification("slack", "warning", "Budget risk", "Projected month end exceeds budget")
    payload = render_slack_payload(event)
    assert "text" in payload
    assert "attachments" in payload
