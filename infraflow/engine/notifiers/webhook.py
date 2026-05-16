import aiohttp
async def send_webhook(url,payload):
    if not url: return
    async with aiohttp.ClientSession() as s:
        await s.post(url, json=payload)
