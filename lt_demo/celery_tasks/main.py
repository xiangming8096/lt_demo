from celery import Celery
import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lt_demo.settings.dev'


celery_app = Celery('lt_demo')
# 配置文件
celery_app.config_from_object('celery_tasks.config')
# 报备任务
celery_app.autodiscover_tasks(['celery_tasks.email', ])
