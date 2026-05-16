from prometheus_client import Counter, Gauge

INGESTED_RECORDS = Counter("cloudbudget_ingested_records_total", "Total ingested cost records", ["provider"])
RECOMMENDATIONS_TOTAL = Counter("cloudbudget_recommendations_total", "Total generated recommendations", ["category"])
BUDGET_UTILIZATION = Gauge("cloudbudget_budget_utilization_pct", "Budget utilization percent", ["tenant_id"])
