from celery import Celery

from celery_tasks.file_creating import create_excel_file
from settings import settings

app = Celery("tasks", backend="rpc://", broker=settings.rabbitmq_path)


@app.task
def start_creating_excel_file(menus: dict):
    return create_excel_file(menus, start_creating_excel_file.request.id)
