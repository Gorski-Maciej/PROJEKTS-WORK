import json
import logging
import time

logger = logging.getLogger(__name__)


class ExfiltrationDetector:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.volume_threshold = 10 * 1024 * 1024

    async def check_volume(self, flow: dict):
        src_ip = flow.get('src_ip')
        dst_ip = flow.get('dst_ip')
        length = int(flow.get('length', 0))
        if not src_ip or not dst_ip or length <= 0:
            return

        now = int(time.time())
        key = f'exfil:{src_ip}:{dst_ip}:{now // 60}'
        total = await self.redis.incrby(key, length)
        await self.redis.expire(key, 120)

        if total >= self.volume_threshold:
            alert = {
                'timestamp': time.time(),
                'type': 'data_exfiltration',
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'bytes_1m': total,
            }
            logger.warning('Potential exfiltration detected: %s', alert)
            await self.redis.rpush('alerts_list', json.dumps(alert))
            await self.redis.ltrim('alerts_list', -1000, -1)
            await self.redis.publish('alerts', json.dumps(alert))
