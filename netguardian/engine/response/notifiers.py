import logging
import os

import aiohttp

logger = logging.getLogger(__name__)
SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


async def send_slack_alert(message: str):
    if not SLACK_WEBHOOK:
        logger.info("Slack webhook not configured")
        return

    async with aiohttp.ClientSession() as session:
        await session.post(SLACK_WEBHOOK, json={"text": message})
