from celery import Celery
from app.core.config import settings

# Create Celery instance
celery_app = Celery(
    "blood_donor_api",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=[
        "app.services.notification_service",
        "app.services.alert_service",
        "app.services.donation_service",
    ],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Configure beat schedule for periodic tasks
celery_app.conf.beat_schedule = {
    # Process scheduled alerts every minute
    "process-scheduled-alerts": {
        "task": "app.services.alert_service.process_scheduled_alerts",
        "schedule": 60.0,  # seconds
    },
    # Clean up old notifications daily
    "cleanup-old-notifications": {
        "task": "app.services.notification_service.cleanup_old_notifications",
        "schedule": 86400.0,  # 24 hours
    },
}

# Import tasks after configuration
from app.services.notification_service import send_notification_task
from app.services.alert_service import (
    process_scheduled_alerts,
    send_alert_notifications,
)
from app.services.donation_service import update_donor_availability
