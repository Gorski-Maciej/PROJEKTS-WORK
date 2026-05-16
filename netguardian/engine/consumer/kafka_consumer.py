import asyncio
import json
import os
import threading
from datetime import datetime, timezone

import redis.asyncio as redis
from confluent_kafka import Consumer, KafkaError

from consumer.enrichment import enrich_flow
from detection.dns_analyzer import DNSAnomalyDetector
from detection.exfiltration import ExfiltrationDetector
from response.executor import trigger_alert

TOPIC = 'netguardian.raw_flows'
KAFKA_BOOTSTRAP = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')


async def start_kafka_consumer(redis_client: redis.Redis, db_pool, duck_con, beacon_detector=None):
    event_loop = asyncio.get_running_loop()
    dns_detector = DNSAnomalyDetector(redis_client)
    exfil_detector = ExfiltrationDetector(redis_client)

    consumer_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP,
        'group.id': 'engine-group',
        'auto.offset.reset': 'latest',
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([TOPIC])

    def poll_loop():
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                print(f'Kafka error: {msg.error()}')
                break
            try:
                flow = json.loads(msg.value().decode())
                fut = store_flow(redis_client, db_pool, duck_con, flow, dns_detector, exfil_detector, beacon_detector)
                asyncio.run_coroutine_threadsafe(fut, event_loop)
            except Exception as exc:  # noqa: BLE001
                print(f'Error processing message: {exc}')

    threading.Thread(target=poll_loop, daemon=True).start()
    await asyncio.sleep(1)


async def store_flow(redis_conn: redis.Redis, db_pool, duck_con, flow: dict, dns_detector: DNSAnomalyDetector, exfil_detector: ExfiltrationDetector, beacon_detector=None):
    flow = await enrich_flow(flow)
    if flow.get('abuse_score', 0) > 80:
        await trigger_alert(redis_conn, flow.get('src_ip', ''), score=-1.0, features=[], threat_intel=True)

    await redis_conn.xadd('flows', flow)
    await redis_conn.expire('flows', 30)

    if beacon_detector:
        await beacon_detector.record_connection(flow)

    if str(flow.get('proto')) == '17' and str(flow.get('dst_port')) == '53' and flow.get('domain'):
        await dns_detector.analyze_query(flow['domain'])

    await exfil_detector.check_volume(flow)

    ts = datetime.fromtimestamp(float(flow['timestamp']), tz=timezone.utc)
    async with db_pool.acquire() as conn:
        await conn.execute(
            '''
            INSERT INTO flows (time, agent_id, src_ip, dst_ip, src_port, dst_port, proto, flags, length)
            VALUES ($1, $2, $3::inet, $4::inet, $5, $6, $7, $8, $9)
            ''',
            ts,
            flow.get('agent_id'),
            flow.get('src_ip'),
            flow.get('dst_ip'),
            int(flow.get('src_port', 0)),
            int(flow.get('dst_port', 0)),
            int(flow.get('proto', 0)),
            flow.get('flags'),
            int(flow.get('length', 0)),
        )

    duck_con.execute(
        '''
        CREATE TABLE IF NOT EXISTS flows (
            time TIMESTAMP,
            agent_id TEXT,
            src_ip TEXT,
            dst_ip TEXT,
            src_port INTEGER,
            dst_port INTEGER,
            proto INTEGER,
            flags TEXT,
            length INTEGER
        )
        '''
    )
    duck_con.execute(
        'INSERT INTO flows VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (ts.replace(tzinfo=None), flow.get('agent_id'), flow.get('src_ip'), flow.get('dst_ip'), int(flow.get('src_port', 0)), int(flow.get('dst_port', 0)), int(flow.get('proto', 0)), flow.get('flags'), int(flow.get('length', 0))),
    )
