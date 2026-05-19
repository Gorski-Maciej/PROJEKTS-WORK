import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.main import get_costs, get_costs_summary, get_top_costs


def test_cost_summary_total():
    payload = get_costs_summary()
    assert payload["total"] > 0
    assert "period" in payload


def test_cost_filter_by_service():
    costs = get_costs(service="ec2")
    assert costs
    assert all(item["service"] == "EC2" for item in costs)


def test_top_costs_limit():
    top = get_top_costs(limit=2)
    assert len(top) == 2
    assert top[0]["amount"] >= top[1]["amount"]
