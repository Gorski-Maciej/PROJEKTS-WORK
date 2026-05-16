import time
from typing import Callable, TypeVar

T = TypeVar("T")


def retry_call(func: Callable[[], T], retries: int = 3, base_delay: float = 0.05) -> T:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            return func()
        except Exception as exc:  # intentional broad capture for generic retry helper
            last_exc = exc
            if attempt == retries - 1:
                break
            time.sleep(base_delay * (2 ** attempt))
    raise RuntimeError(f"retry_call exhausted retries={retries}") from last_exc
