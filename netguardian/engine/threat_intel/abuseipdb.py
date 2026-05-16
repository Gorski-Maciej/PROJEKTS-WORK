import logging
import os

import aiohttp

logger = logging.getLogger(__name__)
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")


async def check_ip_reputation(ip: str) -> dict:
    if not ABUSEIPDB_API_KEY:
        return {}

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params, timeout=5) as resp:
                if resp.status == 200:
                    payload = await resp.json()
                    return payload.get("data", {})
                logger.warning("AbuseIPDB returned HTTP %s", resp.status)
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed reputation check for %s: %s", ip, exc)
    return {}
