import asyncio
from unittest.mock import AsyncMock, patch

from core.context import RepairContext
from worker.executor import execute_checks_for_server


def test_high_cpu_action():
    async def scenario():
        ctx = RepairContext(db_pool=object(), redis=AsyncMock())
        server = {
            'name': 'test',
            'host': 'x',
            'user': 'root',
            'checks': [{'type': 'cpu', 'actions': [{'type': 'restart_service', 'target': 'nginx', 'condition': 'cpu > 90'}]}],
        }
        with (
            patch('worker.executor.run_ssh', new_callable=AsyncMock) as mock_ssh,
            patch('worker.executor.save_metric', new_callable=AsyncMock),
            patch('worker.executor.log_incident', new_callable=AsyncMock),
        ):
            mock_ssh.return_value = ('95', '', 0)
            await execute_checks_for_server(server, ctx)
            assert mock_ssh.call_count >= 2

    asyncio.run(scenario())
