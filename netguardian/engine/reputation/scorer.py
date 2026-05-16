import logging

logger = logging.getLogger(__name__)


class ReputationScorer:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.weights = {"alert": 10, "scan": 20, "block": 50}

    async def add_event(self, ip: str, event_type: str):
        increment = self.weights.get(event_type, 5)
        new_score = await self.redis.zincrby("reputation_scores", increment, ip)
        if new_score > 100:
            await self.redis.sadd("greylist", ip)
            logger.info("IP %s added to greylist (score=%s)", ip, new_score)
