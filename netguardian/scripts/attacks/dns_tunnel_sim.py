import random
import string
import sys
import time

from dnslib import DNSRecord
import socket

server = sys.argv[1] if len(sys.argv) > 1 else "8.8.8.8"
count = int(sys.argv[2]) if len(sys.argv) > 2 else 100

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

for _ in range(count):
    sub = "".join(random.choices(string.ascii_lowercase + string.digits, k=48))
    qname = f"{sub}.exfil-test.local"
    query = DNSRecord.question(qname).pack()
    sock.sendto(query, (server, 53))
    time.sleep(0.05)

print(f"sent {count} high-entropy DNS queries to {server}")
