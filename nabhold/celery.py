import os
from decouple import config
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nabhold.settings.base")

app = Celery("nabhold")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery Beat Schedule
# Executes every 5 minutes
app.conf.beat_schedule = {
    "fetch-weather-data-every-5-minutes": {
        "task": "celery_tasks.tasks.fetch_weather_data",  # Correct task path
        "schedule": crontab(minute="*/5"),  # Every 5 minutes
    },
}

# Update broker URL to use Redis service name defined in docker-compose.yml
app.conf.update(
    broker_url=config("CELERY_BROKER_URL"),
    result_backend=config("CELERY_RESULT_BACKEND"),
    worker_concurrency=4,  # Adjust based on your system
)


# Ensuring task discovery
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
