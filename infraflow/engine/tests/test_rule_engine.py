from core.rule_engine import evaluate_condition

def test_condition_true():
    assert evaluate_condition('cpu > 90', {'cpu':95})
