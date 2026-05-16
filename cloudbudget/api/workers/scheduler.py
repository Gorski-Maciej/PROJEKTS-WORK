from api.services.tasks import analyze_costs_task


def schedule_daily_analysis(tenant_ids: list[int]) -> list[dict]:
    jobs = []
    for tenant_id in tenant_ids:
        jobs.append(analyze_costs_task.delay(tenant_id))
    return [{"queued": True, "task_id": getattr(j, "id", None)} for j in jobs]


def schedule_weekly_forecast(tenant_ids: list[int]) -> list[dict]:
    jobs = []
    for tenant_id in tenant_ids:
        jobs.append(analyze_costs_task.delay(tenant_id))
    return [{"queued": True, "type": "forecast", "task_id": getattr(j, "id", None)} for j in jobs]
