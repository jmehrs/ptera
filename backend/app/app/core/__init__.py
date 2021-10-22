from app.core.celery_app import celery_app
from app.core.inspector import Inspector
from app.core.config import settings


celery_app.loader.import_default_modules()

# Celery worker/task inspector object
inspector = Inspector(celery_app=celery_app)