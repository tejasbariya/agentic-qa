import os
from celery import Celery
from app.core.config import settings
from app.core.docker_engine import run_test_container

celery_app = Celery(
    "worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0")
)

celery_app.conf.task_routes = {
    "app.worker.execute_tests": "main-queue"
}

@celery_app.task
def execute_tests(repository_url: str, test_command: str):
    return run_test_container(repository_url, test_command)
