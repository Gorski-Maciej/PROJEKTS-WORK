import json
import os
import random
import time

from confluent_kafka import Producer

KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
AGENT_ID = os.getenv("AGENT_ID", "agent-01")
TOPIC = "netguardian.raw_flows"
HEARTBEAT_TOPIC = "netguardian.heartbeats"

producer = Producer({"bootstrap.servers": KAFKA_BOOTSTRAP})


def generate_flow() -> dict:
    """Symuluje pojedynczy przepływ sieciowy (normalny lub atak)."""
    src_ip = f"192.168.{random.randint(1, 10)}.{random.randint(2, 254)}"
    dst_ip = f"10.0.0.{random.randint(1, 5)}"
    proto = random.choice([6, 17])  # TCP lub UDP
    flags = random.choice(["SYN", "ACK", "SYN-ACK", "RST"])
    length = random.randint(40, 1500)
    return {
        "timestamp": time.time(),
        "agent_id": AGENT_ID,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": random.randint(1024, 65535),
        "dst_port": random.choice([80, 443, 22, 53]),
        "proto": proto,
        "flags": flags,
        "length": length,
    }


def simulate_attack() -> list[dict]:
    """Generuje serię pakietów przypominających DDoS."""
    flows = []
    for _ in range(100):
        flow = generate_flow()
        flow["flags"] = "SYN"
        flow["length"] = 40
        flow["dst_port"] = 80
        flows.append(flow)
    return flows


if __name__ == "__main__":
    print(f"Agent {AGENT_ID} starting...")
    last_heartbeat = 0.0
    while True:
        flow = generate_flow()
        producer.produce(TOPIC, json.dumps(flow).encode())
        producer.poll(0)

        now = time.time()
        if now - last_heartbeat >= 15:
            heartbeat = {"agent_id": AGENT_ID, "timestamp": now}
            producer.produce(HEARTBEAT_TOPIC, json.dumps(heartbeat).encode())
            last_heartbeat = now

        if random.random() < 0.1:
            print("Simulating attack...")
            for attack_flow in simulate_attack():
                producer.produce(TOPIC, json.dumps(attack_flow).encode())
            producer.flush()

        time.sleep(random.uniform(0.01, 0.05))
