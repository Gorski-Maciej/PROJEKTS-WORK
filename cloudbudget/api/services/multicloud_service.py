from __future__ import annotations

from typing import Iterable

from agents import aws_agent, azure_agent, gcp_agent, kubernetes_agent, onprem_agent
from api.schemas.common import CostRecordIn

_PROVIDER_MAP = {
    "aws": aws_agent.collect_costs,
    "azure": azure_agent.collect_costs,
    "gcp": gcp_agent.collect_costs,
    "onprem": onprem_agent.collect_costs,
    "kubernetes": kubernetes_agent.collect_costs,
}


def available_providers() -> list[str]:
    return sorted(_PROVIDER_MAP.keys())


def collect_multicloud_costs(tenant_id: int, providers: Iterable[str] | None = None) -> list[CostRecordIn]:
    selected = list(providers) if providers else available_providers()
    rows: list[CostRecordIn] = []

    for provider in selected:
        if provider not in _PROVIDER_MAP:
            raise ValueError(f"Unsupported provider: {provider}")
        for raw in _PROVIDER_MAP[provider](tenant_id=tenant_id):
            rows.append(CostRecordIn.model_validate(raw))
    return rows
