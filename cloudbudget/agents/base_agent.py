from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class NormalizedCostRecord:
    tenant_id: int
    provider: str
    service: str
    resource_id: str
    amount_usd: float
    usage_quantity: float
    collected_at: datetime


def normalize(tenant_id: int, provider: str, service: str, resource_id: str, amount_usd: float, usage_quantity: float = 0.0) -> dict:
    return NormalizedCostRecord(
        tenant_id=tenant_id,
        provider=provider,
        service=service,
        resource_id=resource_id,
        amount_usd=amount_usd,
        usage_quantity=usage_quantity,
        collected_at=datetime.now(timezone.utc),
    ).__dict__
