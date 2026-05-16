from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class BreakerState:
    failures: int = 0
    opened_until: datetime | None = None


class SimpleCircuitBreaker:
    def __init__(self, failure_threshold: int = 3, cooldown_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self.state = BreakerState()

    def is_open(self) -> bool:
        if self.state.opened_until is None:
            return False
        if datetime.now(timezone.utc) >= self.state.opened_until:
            self.state.opened_until = None
            self.state.failures = 0
            return False
        return True

    def record_success(self) -> None:
        self.state.failures = 0
        self.state.opened_until = None

    def record_failure(self) -> None:
        self.state.failures += 1
        if self.state.failures >= self.failure_threshold:
            self.state.opened_until = datetime.now(timezone.utc) + timedelta(seconds=self.cooldown_seconds)
