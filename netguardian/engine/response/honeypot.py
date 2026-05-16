import asyncio
import logging

import docker

logger = logging.getLogger(__name__)


class HoneypotManager:
    def __init__(self):
        self.client = docker.from_env()
        self.active_honeypots = {}

    async def deploy_honeypot(self, target_ip: str, port: int, protocol: str = 'tcp'):
        image = {22: 'cowrie/cowrie:latest', 80: 'nginx:alpine', 445: 'dionaea/dionaea:latest'}.get(port, 'alpine:latest')
        name = f'honeypot-{target_ip}-{port}'
        if name in self.active_honeypots:
            return
        try:
            container = self.client.containers.run(
                image,
                name=name,
                detach=True,
                ports={f'{port}/{protocol}': port},
                environment={'HOST_IP': target_ip},
                remove=True,
            )
            self.active_honeypots[name] = container
            asyncio.create_task(self.auto_remove(name, 900))
            logger.info('Deployed honeypot %s', name)
        except Exception as exc:  # noqa: BLE001
            logger.error('Failed to deploy honeypot: %s', exc)

    async def auto_remove(self, name: str, delay: int):
        await asyncio.sleep(delay)
        container = self.active_honeypots.pop(name, None)
        if container:
            container.stop()
            container.remove()
            logger.info('Honeypot %s removed', name)
