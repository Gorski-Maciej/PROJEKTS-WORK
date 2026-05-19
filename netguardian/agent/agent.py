import json, time, random, os
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092')})

while True:
    flow = {
        "timestamp": time.time(),
        "src_ip": f"192.168.{random.randint(1,10)}.{random.randint(2,254)}",
        "dst_ip": "10.0.0.1",
        "length": random.randint(40, 1500)
    }
    producer.produce('netguardian.raw_flows', json.dumps(flow).encode())
    producer.poll(0)
    time.sleep(random.uniform(0.1, 0.5))
