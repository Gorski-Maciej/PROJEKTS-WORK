from sqlalchemy.orm import Session
from api.models.entities import CostRecord
from api.schemas.common import CostRecordIn
from api.core.metrics import INGESTED_RECORDS


def ingest_cost_records(db: Session, payloads: list[CostRecordIn]) -> int:
    rows = [CostRecord(**p.model_dump()) for p in payloads]
    db.add_all(rows)
    db.commit()
    for p in payloads:
        INGESTED_RECORDS.labels(provider=p.provider).inc()
    return len(rows)
