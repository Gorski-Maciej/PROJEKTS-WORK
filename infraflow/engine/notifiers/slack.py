import os, aiohttp
async def send_slack_alert(message):
    webhook=os.getenv('SLACK_WEBHOOK')
    if not webhook: return
    async with aiohttp.ClientSession() as s:
        await s.post(webhook, json={'text':message})
