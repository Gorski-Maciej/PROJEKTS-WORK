import asyncio
import json
import os
import threading
from datetime import datetime, timezone

from confluent_kafka import Consumer, KafkaError

HEARTBEAT_TOPIC = 'netguardian.heartbeats'
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')


async def start_heartbeat_consumer(redis_client):
    event_loop = asyncio.get_running_loop()

    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP,
        'group.id': 'engine-heartbeat-group',
        'auto.offset.reset': 'latest',
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([HEARTBEAT_TOPIC])

    def poll_loop():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f'Heartbeat kafka error: {msg.error()}')
                break
            try:
                payload = json.loads(msg.value().decode())
                fut = store_heartbeat(redis_client, payload)
                asyncio.run_coroutine_threadsafe(fut, event_loop)
            except Exception as exc:  # noqa: BLE001
                print(f'Heartbeat processing error: {exc}')

    threading.Thread(target=poll_loop, daemon=True).start()
    await asyncio.sleep(1)


async def store_heartbeat(redis_client, payload: dict):
    agent_id = payload.get('agent_id')
    if not agent_id:
        return
    timestamp = payload.get('timestamp')
    if not timestamp:
        timestamp = datetime.now(timezone.utc).isoformat()
    key = f'agent:heartbeat:{agent_id}'
    await redis_client.set(key, timestamp, ex=30)
