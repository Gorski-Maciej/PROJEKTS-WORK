from response.executor import _extract_trigger_context, should_execute_playbook


def test_should_execute_playbook_true_on_ddos_like_features():
    playbook = {'trigger': 'anomaly_score < -0.2 AND syn_flood == true'}
    context = _extract_trigger_context(-0.5, ['ddos', 'syn flood'])
    assert should_execute_playbook(playbook, context) is True


def test_should_execute_playbook_false_when_trigger_not_met():
    playbook = {'trigger': 'anomaly_score < -0.2 AND syn_flood == true'}
    context = _extract_trigger_context(-0.1, ['normal'])
    assert should_execute_playbook(playbook, context) is False
