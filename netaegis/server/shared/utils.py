import hashlib
import time

def correlation_id() -> str:
    return hashlib.sha256(str(time.time()).encode()).hexdigest()[:10]
