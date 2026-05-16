from fastapi import FastAPI
from api.core.config import settings
from api.core.database import Base, engine
from api.routers import (
    health,
    costs,
    recommendations,
    simulations,
    budgets,
    predictions,
    realtime,
    actions,
    alerts,
    invoices,
    graphql_api,
    metrics,
    exports,
    reconciliation,
    auth,
    optimizations,
    chargeback,
    autopilot,
    notifications,
    kubernetes,
    invoice_reconciliation,
    reports,
    whatif, dlq,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name, version="2.2.0")
app.include_router(health.router, prefix=settings.api_prefix)
app.include_router(costs.router, prefix=settings.api_prefix)
app.include_router(recommendations.router, prefix=settings.api_prefix)
app.include_router(simulations.router, prefix=settings.api_prefix)
app.include_router(budgets.router, prefix=settings.api_prefix)
app.include_router(predictions.router, prefix=settings.api_prefix)
app.include_router(actions.router, prefix=settings.api_prefix)
app.include_router(alerts.router, prefix=settings.api_prefix)
app.include_router(invoices.router, prefix=settings.api_prefix)
app.include_router(graphql_api.router, prefix=settings.api_prefix)
app.include_router(metrics.router)
app.include_router(exports.router, prefix=settings.api_prefix)
app.include_router(reconciliation.router, prefix=settings.api_prefix)
app.include_router(auth.router, prefix=settings.api_prefix)
app.include_router(optimizations.router, prefix=settings.api_prefix)
app.include_router(chargeback.router, prefix=settings.api_prefix)
app.include_router(autopilot.router, prefix=settings.api_prefix)
app.include_router(notifications.router, prefix=settings.api_prefix)
app.include_router(kubernetes.router, prefix=settings.api_prefix)
app.include_router(invoice_reconciliation.router, prefix=settings.api_prefix)
app.include_router(reports.router, prefix=settings.api_prefix)
app.include_router(whatif.router, prefix=settings.api_prefix)
app.include_router(dlq.router, prefix=settings.api_prefix)
app.include_router(realtime.router)


@app.get("/")
async def root() -> dict:
    return {"service": "cloudbudget", "version": "2.2.0"}
