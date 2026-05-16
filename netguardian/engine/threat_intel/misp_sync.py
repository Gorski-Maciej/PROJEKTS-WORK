import os

import aiohttp

MISP_URL = os.getenv('MISP_URL')
MISP_KEY = os.getenv('MISP_KEY')


async def fetch_iocs():
    if not MISP_URL or not MISP_KEY:
        return []

    headers = {'Authorization': MISP_KEY, 'Accept': 'application/json'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{MISP_URL}/attributes/restSearch', headers=headers, timeout=10) as resp:
                if resp.status == 200:
                    payload = await resp.json()
                    iocs = []
                    for attr in payload.get('response', {}).get('Attribute', []):
                        if attr.get('type') in ('ip-src', 'ip-dst', 'domain'):
                            value = attr.get('value')
                            if value:
                                iocs.append(value)
                    return iocs
    except Exception:
        return []
    return []


async def sync_blacklist(redis_client):
    iocs = await fetch_iocs()
    for ioc in iocs:
        await redis_client.sadd('blacklist:ips', ioc)
