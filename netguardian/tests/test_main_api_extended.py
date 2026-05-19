import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from engine.main import AlertIn, create_alert, get_alerts


def test_create_alert_and_filter():
    created = create_alert(AlertIn(message="Suspicious repeated login attempts", severity="high"))
    assert created["id"] >= 1
    assert "created_at" in created

    filtered = get_alerts(min_severity="high")
    assert any(item["severity"] in ("high", "critical") for item in filtered)
