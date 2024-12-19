from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
app = Celery('web')  
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_url = 'redis://localhost:6379/2'
app.conf.result_backend = 'redis://localhost:6379/2'
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['json' , 'pickle'] 
app.conf.worker_prefetch_muliplier = 1


# app.conf.beat_schedule = {
#     'workflow-amount-checker': {
#         'task': 'core.tasks.workflow_amount_checker_task', 
#         'schedule': crontab(hour='*/1'), 
#     },
# }


