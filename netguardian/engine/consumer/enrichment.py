import json
import os

import redis.asyncio as redis

from enrichment.geoip import get_geo
from threat_intel.abuseipdb import check_ip_reputation

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


async def enrich_flow(flow: dict):
    client = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
    src_ip = flow.get("src_ip")
    if not src_ip:
        return flow

    cache_key = f"threat:{src_ip}"
    cached = await client.get(cache_key)
    if cached:
        rep = json.loads(cached)
    else:
        rep = await check_ip_reputation(src_ip)
        await client.setex(cache_key, 3600, json.dumps(rep))

    flow["abuse_score"] = rep.get("abuseConfidenceScore", 0)
    flow["geo"] = get_geo(src_ip)
    await client.close()
    return flow
