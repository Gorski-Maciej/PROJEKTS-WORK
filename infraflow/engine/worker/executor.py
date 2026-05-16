from __future__ import annotations

import asyncio
import json
from typing import Any

from core.ansible_runner import run_ansible_playbook
from core.rule_engine import evaluate_condition
from core.ssh_client import run_ssh
from core.winrm_client import run_winrm
from database.db import detect_anomalies, log_incident, save_metric
from metrics.prometheus import INCIDENT_COUNTER
from notifiers.email_notifier import send_email
from notifiers.slack import send_slack_alert
from notifiers.webhook import send_webhook




async def run_remote(server: dict[str, Any], command: str) -> tuple[str, str, int]:
    host, user, key = server['host'], server['user'], server.get('key_file')
    if server.get('platform', 'linux').lower() == 'windows':
        return await run_winrm(host, command, user, server.get('password', ''))
    return await run_ssh(host, command, user, key)


async def run_check(server: dict[str, Any], check: dict[str, Any]) -> Any:
    host, user, key = server['host'], server['user'], server.get('key_file')
    check_type = check['type']

    if check_type == 'cpu':
        out, _, _ = await run_remote(server, "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'")
        return float(out or 0)
    if check_type == 'memory':
        out, _, _ = await run_remote(server, "free | grep Mem | awk '{print $3/$2 * 100.0}'")
        return float(out or 0)
    if check_type == 'disk':
        path = check.get('path', '/')
        out, _, _ = await run_remote(server, f"df -h {path} | tail -1 | awk '{{print $5}}' | tr -d '%'")
        return float(out or 0)
    if check_type == 'service':
        out, _, _ = await run_remote(server, f"systemctl is-active {check['name']}")
        return out.strip()
    if check_type == 'port':
        port = check['port']
        out, _, _ = await run_remote(server, f"nc -z -w2 127.0.0.1 {port} && echo open || echo closed")
        return out.strip()
    if check_type == 'package_updates':
        params = check.get('params', {})
        manager = params.get('manager', check.get('manager', 'apt'))
        if manager in ('apt', 'apt-get'):
            cmd = "apt-get -s upgrade 2>/dev/null | grep '^Inst ' | wc -l"
        elif manager in ('yum', 'dnf'):
            cmd = f"{manager} check-update 2>/dev/null | grep -v '^$' | wc -l"
        elif manager == 'zypper':
            cmd = "zypper list-updates 2>/dev/null | grep '|' | wc -l"
        else:
            return None
        out, _, _ = await run_remote(server, cmd)
        return float(out or 0)
    if check_type == 'ansible_playbook':
        playbook = f"/app/config/playbooks/{check['playbook']}"
        rc, _, _ = run_ansible_playbook(playbook, extra_vars={'host': host})
        return float(rc)
    return None


async def execute_action(server: dict[str, Any], action: dict[str, Any], ctx: Any, metric_value: Any = None) -> None:
    host, user, key = server['host'], server['user'], server.get('key_file')
    atype = action['type']
    if atype == 'restart_service':
        await run_remote(server, f"systemctl restart {action['target']}")
    elif atype == 'clean_logs':
        await run_remote(server, f"find {action['path']} -name '*.log' -mtime +7 -delete")
    elif atype == 'send_slack':
        message = action.get('message', 'InfraFlow alert').replace('{server.name}', server['name']).replace('{metric}', str(metric_value))
        await send_slack_alert(message)
    elif atype == 'send_email':
        await send_email(server.get('alerting', {}).get('email', 'admin@example.com'), f'InfraFlow alert for {server["name"]}', str(metric_value))
    elif atype == 'send_webhook':
        await send_webhook(server.get('alerting', {}).get('webhook', ''), {'server': server['name'], 'value': metric_value})
    elif atype == 'run_ansible':
        run_ansible_playbook(f"/app/config/playbooks/{action['playbook']}", extra_vars={'host': host})
    elif atype == 'auto_patch':
        params = action.get('params', {})
        manager = params.get('manager', action.get('manager', 'apt'))
        if manager == 'apt':
            cmds = [
                'export DEBIAN_FRONTEND=noninteractive',
                'apt-get update -qq',
                'apt-get upgrade -y -qq',
                'apt-get autoremove -y -qq',
            ]
        elif manager == 'yum':
            cmds = ['yum update -y', 'yum autoremove -y']
        elif manager == 'dnf':
            cmds = ['dnf upgrade -y', 'dnf autoremove -y']
        elif manager == 'zypper':
            cmds = ['zypper refresh', 'zypper update -y']
        else:
            raise ValueError(f'Unsupported package manager: {manager}')
        await run_remote(server, ' && '.join(cmds))

    priority = action.get('priority', 'info')
    INCIDENT_COUNTER.labels(server=server['name'], priority=priority).inc()
    await log_incident(ctx.db_pool, server['name'], f'Action executed: {atype}', priority)


async def execute_checks_for_server(server: dict[str, Any], ctx: Any) -> None:
    failed_checks = 0
    for check in server.get('checks', []):
        value = await run_check(server, check)
        if value is None:
            continue

        threshold = check.get('threshold')
        if isinstance(threshold, (int, float)) and isinstance(value, (int, float)) and value > threshold:
            failed_checks += 1

        if isinstance(value, (int, float)):
            await save_metric(ctx.db_pool, server['name'], check['type'], float(value))
            if check['type'] == 'cpu':
                if await detect_anomalies(ctx.db_pool, server['name']):
                    await log_incident(ctx.db_pool, server['name'], 'ML anomaly detected on CPU baseline', 'warning')

        context = {
            'cpu': value if check['type'] == 'cpu' else 0,
            'memory': value if check['type'] == 'memory' else 0,
            'disk_usage': value if check['type'] == 'disk' else 0,
            'service_status': value if check['type'] == 'service' else 'unknown',
            'port_status': value if check['type'] == 'port' else 'unknown',
            'available_updates': value if check['type'] == 'package_updates' else 0,
            'failed_checks': failed_checks,
        }

        for action in check.get('actions', []):
            if evaluate_condition(action.get('condition', 'True'), context):
                await execute_action(server, action, ctx, value)

        if ctx.redis is not None:
            await ctx.redis.publish('server_updates', json.dumps({'server': server['name'], 'check': check['type'], 'value': value}))

        await asyncio.sleep(0)
