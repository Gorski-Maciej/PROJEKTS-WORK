from core.rule_engine import evaluate_condition


def test_placeholder():
    assert evaluate_condition('1 < 2', {})
