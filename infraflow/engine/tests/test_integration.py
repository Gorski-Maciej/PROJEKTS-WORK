import asyncio
from unittest.mock import AsyncMock, patch

from core.context import RepairContext
from worker.queue_worker import process_job


def test_high_cpu_triggers_restart():
    async def scenario():
        ctx = RepairContext(db_pool=object(), redis=AsyncMock())
        server = {
            'name': 'test-server',
            'host': 'x',
            'user': 'root',
            'checks': [
                {'type': 'cpu', 'threshold': 80, 'actions': [{'type': 'restart_service', 'target': 'nginx', 'condition': 'cpu > 90'}]}
            ],
        }
        with (
            patch('worker.executor.run_remote', new_callable=AsyncMock) as mock_remote,
            patch('worker.executor.save_metric', new_callable=AsyncMock),
            patch('worker.executor.log_incident', new_callable=AsyncMock),
            patch('worker.executor.detect_anomalies', new_callable=AsyncMock),
        ):
            mock_remote.side_effect = [('95.5', '', 0), ('', '', 0)]
            await process_job({'server': server}, ctx)
            assert any('systemctl restart nginx' in str(c) for c in mock_remote.call_args_list)

    asyncio.run(scenario())
