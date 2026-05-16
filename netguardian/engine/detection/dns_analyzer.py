import json
import logging
import math
import time
from collections import Counter

logger = logging.getLogger(__name__)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    count = Counter(s)
    length = len(s)
    entropy = 0.0
    for freq in count.values():
        p = freq / length
        entropy -= p * math.log2(p)
    return entropy


class DNSAnomalyDetector:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.threshold = 4.5

    async def analyze_query(self, domain: str):
        entropy = shannon_entropy(domain)
        if entropy > self.threshold and len(domain) > 30:
            alert = {
                "timestamp": time.time(),
                "type": "dns_tunnel",
                "domain": domain,
                "entropy": entropy,
            }
            logger.warning("DNS tunnel detected: %s", alert)
            await self.redis.rpush("alerts_list", json.dumps(alert))
            await self.redis.ltrim("alerts_list", -1000, -1)
            await self.redis.publish("alerts", json.dumps(alert))
