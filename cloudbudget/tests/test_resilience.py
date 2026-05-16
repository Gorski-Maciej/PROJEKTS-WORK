from api.services.circuit_breaker import SimpleCircuitBreaker
from api.services.retry import retry_call


def test_circuit_breaker_opens_after_threshold():
    breaker = SimpleCircuitBreaker(failure_threshold=2, cooldown_seconds=1)
    breaker.record_failure()
    assert breaker.is_open() is False
    breaker.record_failure()
    assert breaker.is_open() is True


def test_retry_call_succeeds_after_transient_failures():
    state = {"n": 0}

    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("temporary")
        return "ok"

    assert retry_call(flaky, retries=4) == "ok"
