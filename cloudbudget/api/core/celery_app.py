from celery import Celery
from api.core.config import settings

celery_app = Celery("cloudbudget", broker=settings.rabbitmq_url, backend=settings.redis_url)
celery_app.conf.task_routes = {
    "api.services.tasks.ingest_costs_task": {"queue": "cost.ingest"},
    "api.services.tasks.analyze_costs_task": {"queue": "cost.analyze"},
    "api.services.tasks.execute_action_task": {"queue": "action.exec"},
}
