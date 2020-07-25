from celery import Celery

app = Celery('celery_tasks') # 实例化celery对象

app.config_from_object('celery_tasks.celeryconfig') # 配置文件加载
