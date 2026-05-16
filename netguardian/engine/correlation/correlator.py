import json
import logging
import time

logger = logging.getLogger(__name__)


class EventCorrelator:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.window = 60

    async def process_alert(self, alert: dict):
        src_ip = alert.get("src_ip")
        if not src_ip:
            return

        key = f"corr:{src_ip}"
        await self.redis.rpush(key, json.dumps(alert))
        await self.redis.expire(key, self.window)

        raw_alerts = await self.redis.lrange(key, 0, -1)
        alerts = [json.loads(a) for a in raw_alerts]

        unique_targets = set()
        for item in alerts:
            dst = item.get("dst_ip") or item.get("details", {}).get("dst_ip")
            if dst:
                unique_targets.add(dst)

        if len(unique_targets) >= 3:
            incident = {
                "type": "correlated_scan",
                "src_ip": src_ip,
                "targets": list(unique_targets),
                "count": len(alerts),
                "timestamp": time.time(),
            }
            logger.warning("Correlated incident: %s", incident)
            await self.redis.publish("alerts", json.dumps(incident))
