
import os
from celery import Celery

# Инициализируем приложение Celery
# broker='redis://redis:6379/0' — имя 'redis' должно совпадать с названием сервиса в docker-compose.yml
celery_app = Celery(
    'inventory_service',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Настройки
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Moscow',
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    include=['app.tasks'] 
)

# Если у тебя задачи будут лежать в разных папках, эта строка поможет их найти
celery_app.autodiscover_tasks()

