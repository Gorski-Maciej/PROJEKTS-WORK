from datetime import datetime, timezone
from sqlalchemy.orm import Session
from api.services.analytics_service import cost_summary
from api.services.budget_service import budget_status
from api.services.prediction_service import forecast_for_tenant


def build_finops_report(db: Session, tenant_id: int) -> dict:
    summary = cost_summary(db, tenant_id)
    budget = budget_status(db, tenant_id)
    forecast = forecast_for_tenant(db, tenant_id)
    generated_at = datetime.now(timezone.utc).isoformat()
    report_text = (
        f"CloudBudget FinOps Report\n"
        f"Tenant: {tenant_id}\n"
        f"Generated: {generated_at}\n"
        f"Monthly total: {summary.get('monthly_total', 0):.2f} USD\n"
        f"Budget state: {budget.get('state', 'unknown')}\n"
        f"Forecast (30d): {forecast.get('prediction_30d', 0):.2f} USD\n"
    )
    return {
        "tenant_id": tenant_id,
        "generated_at": generated_at,
        "summary": summary,
        "budget": budget,
        "forecast": forecast,
        "report_text": report_text,
    }
