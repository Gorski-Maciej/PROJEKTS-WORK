from agents.aws_agent import collect_costs


def test_aws_agent_returns_normalized_rows():
    rows = collect_costs(tenant_id=7)
    assert rows and rows[0]["tenant_id"] == 7 and rows[0]["provider"] == "aws"
