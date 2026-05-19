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
    skip_geoip = os.getenv("SKIP_GEOIP_CHECK", "true").lower() == "true"
    geoip_db = os.getenv("GEOIP_DB", "/app/data/GeoLite2-City.mmdb")
    if skip_geoip:
        logger.info("Skipping GeoIP DB validation (SKIP_GEOIP_CHECK=true)")
    else:
        try:
            with open(geoip_db, "rb"):
                logger.info("GeoIP DB detected at %s", geoip_db)
        except Exception as exc:
            logger.warning("GeoIP DB unavailable at %s: %s", geoip_db, exc)
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
