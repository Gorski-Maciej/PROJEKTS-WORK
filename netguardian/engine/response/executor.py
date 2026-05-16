import asyncio
import json
import logging
import os
import time

import paramiko
import redis.asyncio as redis
import yaml

from correlation.correlator import EventCorrelator
from reputation.scorer import ReputationScorer
from response.honeypot import HoneypotManager
from response.notifiers import send_slack_alert

logger = logging.getLogger(__name__)
PLAYBOOK_DIR = os.path.join(os.path.dirname(__file__), 'playbooks')
SSH_KEY_FILE = os.getenv('SSH_PRIVATE_KEY_FILE', '/app/ssh/id_rsa')
SSH_AGENT_HOST = os.getenv('SSH_AGENT_HOST', 'agent')
SSH_AGENT_USER = os.getenv('SSH_AGENT_USER', 'root')
_honeypot_manager = None


def get_honeypot_manager():
    global _honeypot_manager
    if _honeypot_manager is None:
        _honeypot_manager = HoneypotManager()
    return _honeypot_manager




def _normalize_trigger_expression(expr: str) -> str:
    return expr.replace('AND', 'and').replace('OR', 'or').replace('true', 'True').replace('false', 'False')


def _extract_trigger_context(score: float, features: list) -> dict:
    text = ' '.join(str(f).lower() for f in (features or []))
    return {
        'anomaly_score': score,
        'syn_flood': 'syn' in text and ('flood' in text or 'ddos' in text),
    }


def should_execute_playbook(playbook: dict, context: dict) -> bool:
    expr = playbook.get('trigger')
    if not expr:
        return True
    safe_expr = _normalize_trigger_expression(str(expr))
    try:
        return bool(eval(safe_expr, {'__builtins__': {}}, context))
    except Exception as exc:  # noqa: BLE001
        logger.error('Invalid playbook trigger %r: %s', expr, exc)
        return False


async def trigger_alert(redis_client: redis.Redis, src_ip: str, score: float, features: list, threat_intel: bool = False):
    alert = {
        'timestamp': time.time(),
        'src_ip': src_ip,
        'score': score,
        'features': features,
        'action': 'alert',
        'threat_intel': threat_intel,
    }
    logger.warning('Anomaly detected: %s', alert)
    await redis_client.rpush('alerts_list', json.dumps(alert))
    await redis_client.ltrim('alerts_list', -1000, -1)
    await redis_client.publish('alerts', json.dumps(alert))

    correlator = EventCorrelator(redis_client)
    scorer = ReputationScorer(redis_client)
    await correlator.process_alert(alert)
    await scorer.add_event(src_ip, 'alert')

    playbook = load_playbook('ddos.yml')
    context = _extract_trigger_context(score, features)
    if should_execute_playbook(playbook, context):
        await execute_playbook(redis_client, src_ip, playbook)
    else:
        logger.info('Playbook trigger not matched for %s with context %s', src_ip, context)


def load_playbook(name: str):
    with open(os.path.join(PLAYBOOK_DIR, name), 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def _execute_ssh_command(host: str, command: str, username: str, key_file: str):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, username=username, key_filename=key_file)
        _, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if err:
            logger.error('SSH error: %s', err)
        return out
    except Exception as exc:  # noqa: BLE001
        logger.error('SSH connection failed: %s', exc)
        return ''
    finally:
        ssh.close()


async def execute_ssh_command(host: str, command: str, username: str = SSH_AGENT_USER, key_file: str = SSH_KEY_FILE):
    return await asyncio.to_thread(_execute_ssh_command, host, command, username, key_file)


async def execute_playbook(redis_client: redis.Redis, src_ip: str, playbook: dict, agent_host: str = SSH_AGENT_HOST):
    scorer = ReputationScorer(redis_client)
    for action in playbook.get('actions', []):
        if action['type'] == 'block_ip':
            duration = action.get('params', {}).get('duration', 600)
            cmd = f'iptables -A INPUT -s {src_ip} -j DROP && sleep {duration} && iptables -D INPUT -s {src_ip} -j DROP'
            asyncio.create_task(execute_ssh_command(agent_host, cmd))
            await redis_client.sadd('blocked_ips', src_ip)
            await scorer.add_event(src_ip, 'block')
        elif action['type'] == 'notify_slack':
            message = action.get('params', {}).get('message', '').replace('{{ src_ip }}', src_ip)
            await send_slack_alert(message)
        elif action['type'] == 'deploy_honeypot':
            port = action.get('params', {}).get('port', 80)
            await get_honeypot_manager().deploy_honeypot(src_ip, port)
        elif action['type'] == 'capture_pcap':
            logger.info('Starting PCAP capture for %s', src_ip)
