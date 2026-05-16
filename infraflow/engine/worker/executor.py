from __future__ import annotations

import json
from typing import Any

from core.ansible_runner import run_ansible_playbook
from core.rule_engine import evaluate_condition
from core.ssh_client import run_ssh
from database.db import log_incident, save_metric
from metrics.prometheus import INCIDENT_COUNTER
from notifiers.email_notifier import send_email
from notifiers.slack import send_slack_alert
from notifiers.webhook import send_webhook


async def run_check(server: dict[str, Any], check: dict[str, Any]) -> Any:
    host, user, key = server['host'], server['user'], server.get('key_file')
    if check['type'] == 'cpu':
        out, _, _ = await run_ssh(host, "top -bn1 | grep 'Cpu(s)' | awk '{print $2+$4}'", user, key)
        return float(out or 0)
    if check['type'] == 'memory':
        out, _, _ = await run_ssh(host, "free | grep Mem | awk '{print $3/$2 * 100.0}'", user, key)
        return float(out or 0)
    if check['type'] == 'disk':
        path = check.get('path', '/')
        out, _, _ = await run_ssh(host, f"df -h {path} | tail -1 | awk '{{print $5}}' | tr -d '%'", user, key)
        return float(out or 0)
    if check['type'] == 'service':
        out, _, _ = await run_ssh(host, f"systemctl is-active {check['name']}", user, key)
        return out.strip()
    return None


async def execute_action(server: dict[str, Any], action: dict[str, Any], ctx: Any, metric_value: Any = None) -> None:
    host, user, key = server['host'], server['user'], server.get('key_file')
    atype = action['type']
    if atype == 'restart_service':
        await run_ssh(host, f"systemctl restart {action['target']}", user, key)
    elif atype == 'clean_logs':
        await run_ssh(host, f"find {action['path']} -name '*.log' -mtime +7 -delete", user, key)
    elif atype == 'send_slack':
        message = action.get('message', 'InfraFlow alert').replace('{server.name}', server['name']).replace('{metric}', str(metric_value))
        await send_slack_alert(message)
    elif atype == 'send_email':
        await send_email(server.get('alerting', {}).get('email', 'admin@example.com'), f'InfraFlow alert for {server["name"]}', str(metric_value))
    elif atype == 'send_webhook':
        await send_webhook(server.get('alerting', {}).get('webhook', ''), {'server': server['name'], 'value': metric_value})
    elif atype == 'run_ansible':
        run_ansible_playbook(f"/app/config/playbooks/{action['playbook']}", extra_vars={'host': host})

    priority = action.get('priority', 'info')
    INCIDENT_COUNTER.labels(server=server['name'], priority=priority).inc()
    await log_incident(ctx.db_pool, server['name'], f'Action executed: {atype}', priority)


async def execute_checks_for_server(server: dict[str, Any], ctx: Any) -> None:
    for check in server.get('checks', []):
        value = await run_check(server, check)
        if value is None:
            continue

        if isinstance(value, (int, float)):
            await save_metric(ctx.db_pool, server['name'], check['type'], float(value))

        context = {
            'cpu': value if check['type'] == 'cpu' else 0,
            'memory': value if check['type'] == 'memory' else 0,
            'disk_usage': value if check['type'] == 'disk' else 0,
            'service_status': value if check['type'] == 'service' else 'unknown',
        }

        for action in check.get('actions', []):
            if evaluate_condition(action.get('condition', 'True'), context):
                await execute_action(server, action, ctx, value)

        if ctx.redis is not None:
            await ctx.redis.publish('server_updates', json.dumps({'server': server['name'], 'check': check['type'], 'value': value}))
