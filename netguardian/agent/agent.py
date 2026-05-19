from __future__ import annotations

import json
import os
import random
import time

from confluent_kafka import Producer

bootstrap = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
topic = "netguardian.raw_flows"
producer = Producer({"bootstrap.servers": bootstrap})


while True:
    payload = {
        "src_ip": f"10.0.0.{random.randint(1, 254)}",
        "dst_ip": f"192.168.1.{random.randint(1, 254)}",
        "bytes": random.randint(64, 2048),
        "protocol": random.choice(["TCP", "UDP"]),
    }
    producer.produce(topic, json.dumps(payload).encode("utf-8"))
    producer.flush()
    print(f"sent flow to {topic}: {payload}")
    time.sleep(5)
