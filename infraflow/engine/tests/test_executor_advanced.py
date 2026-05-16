import asyncio
from unittest.mock import AsyncMock, patch

from core.context import RepairContext
from worker.executor import execute_checks_for_server


def test_failed_checks_enables_conditional_action():
    async def scenario():
        ctx = RepairContext(db_pool=object(), redis=AsyncMock())
        server = {
            'name': 'web1',
            'host': 'host',
            'user': 'root',
            'checks': [
                {
                    'type': 'cpu',
                    'threshold': 80,
                    'actions': [
                        {'type': 'restart_service', 'target': 'nginx', 'condition': 'failed_checks > 0'}
                    ],
                }
            ],
        }

        with (
            patch('worker.executor.run_ssh', new_callable=AsyncMock) as mock_ssh,
            patch('worker.executor.save_metric', new_callable=AsyncMock),
            patch('worker.executor.log_incident', new_callable=AsyncMock),
        ):
            mock_ssh.return_value = ('95', '', 0)
            await execute_checks_for_server(server, ctx)
            calls = [str(c) for c in mock_ssh.call_args_list]
            assert any('systemctl restart nginx' in c for c in calls)

    asyncio.run(scenario())
