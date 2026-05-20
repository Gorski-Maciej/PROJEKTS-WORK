import json
import logging
import os
import random
import signal
import time

from confluent_kafka import Producer


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("netguardian-agent")

_running = True


def _shutdown_handler(signum, _frame):
    global _running
    logger.info("received signal %s, stopping agent loop", signum)
    _running = False


signal.signal(signal.SIGTERM, _shutdown_handler)
signal.signal(signal.SIGINT, _shutdown_handler)

producer = Producer({"bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")})
topic = os.getenv("KAFKA_TOPIC", "netguardian.raw_flows")

logger.info("starting traffic flow generator on topic=%s", topic)

while _running:
    flow = {
        "timestamp": time.time(),
        "src_ip": f"192.168.{random.randint(1,10)}.{random.randint(2,254)}",
        "dst_ip": "10.0.0.1",
        "length": random.randint(40, 1500),
    }
    payload = json.dumps(flow).encode()

    try:
        producer.produce(topic, payload)
    except BufferError:
        logger.warning("producer queue full, polling and retrying")
        producer.poll(1)
        producer.produce(topic, payload)

    producer.poll(0)
    time.sleep(random.uniform(0.1, 0.5))

logger.info("flushing producer before exit")
producer.flush(5)
logger.info("agent stopped")
