from __future__ import annotations

import asyncio
import json
import logging
import os

from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("netguardian")
app = FastAPI(title="NetGuardian API")


async def kafka_consumer_simulator() -> None:
    topic = os.getenv("KAFKA_TOPIC", "netguardian.raw_flows")
    while True:
        message = {"topic": topic, "payload": "simulated-packet"}
        logger.info("Kafka message received: %s", json.dumps(message))
        await asyncio.sleep(5)


@app.on_event("startup")
async def startup_event() -> None:
    asyncio.create_task(kafka_consumer_simulator())


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "netguardian-engine"}


@app.get("/api/v1/alerts")
async def get_alerts() -> dict[str, list[dict[str, str]]]:
    return {
        "alerts": [
            {"severity": "high", "message": "Potential port scan detected"},
            {"severity": "medium", "message": "Unusual DNS query volume"},
        ]
    }
