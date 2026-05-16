from api.core.celery_app import celery_app


@celery_app.task
def ingest_costs_task(records: list[dict]) -> dict:
    return {"ingested": len(records)}


@celery_app.task
def analyze_costs_task(tenant_id: int) -> dict:
    return {"tenant_id": tenant_id, "status": "analysis_scheduled"}


@celery_app.task
def execute_action_task(action: dict) -> dict:
    return {"status": "queued", "action": action}
