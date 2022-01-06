from app.core.config import settings

broker_url = settings.CELERY_BROKER_URL
result_backend = settings.CELERY_BACKEND_URL
result_expires = 3600

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
