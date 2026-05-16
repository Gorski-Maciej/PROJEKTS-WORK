import json
import logging
import time

import numpy as np

logger = logging.getLogger(__name__)


class BeaconDetector:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.window = 3600
        self.min_beacon_interval = 10
        self.max_beacon_interval = 3600
        self.min_connections = 5

    async def analyze_beacons(self):
        keys = await self.redis.keys("conn:*")
        for key in keys:
            src_dst = key.split(":", 1)[1]
            if "-" not in src_dst:
                continue
            src_ip, dst_ip = src_dst.split("-", 1)
            timestamps = sorted(float(t) for t in await self.redis.lrange(key, 0, -1))
            if len(timestamps) < self.min_connections:
                continue

            intervals = np.diff(timestamps)
            if len(intervals) < 3:
                continue

            std_interval = float(np.std(intervals))
            mean_interval = float(np.mean(intervals))
            if mean_interval == 0:
                continue

            cv = std_interval / mean_interval
            if cv < 0.2 and self.min_beacon_interval <= mean_interval <= self.max_beacon_interval:
                alert = {
                    "timestamp": time.time(),
                    "type": "beaconing",
                    "src_ip": src_ip,
                    "dst_ip": dst_ip,
                    "mean_interval": mean_interval,
                    "certainty": 1 - cv,
                }
                logger.warning("Beaconing detected: %s", alert)
                await self.redis.rpush("alerts_list", json.dumps(alert))
                await self.redis.publish("alerts", json.dumps(alert))

    async def record_connection(self, flow: dict):
        src = flow.get("src_ip")
        dst = flow.get("dst_ip")
        ts = flow.get("timestamp")
        if not src or not dst or ts is None:
            return
        key = f"conn:{src}-{dst}"
        await self.redis.rpush(key, ts)
        await self.redis.expire(key, self.window)
