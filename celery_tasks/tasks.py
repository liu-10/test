from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
# from goods.models import GoodsType,IndexGoodsBanner,IndexPtomotionBanner
from django_redis import get_redis_connection
from django.template import loader, RequestContext
import time

# 任务处理者加
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quickbutton.settings')
django.setup()

import sys
sys.setrecursionlimit(10000)

# 创建一个对象,括号内为路径
app = Celery('celery_tasks.tasks', broker='redis://:123456@127.0.0.1:6379/9')
app.config_from_object('celery_tasks.celeryconfig')      #引入配置文件
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)



@app.task
# 定义任务函数
def send_email(to_email,username,token):
    """发送激活邮件"""
    subject = 'xxx欢迎您'
    message = ''
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    html_message = '<h1>%s,欢迎您成为xxx的注册用户</h1>请点击下面的激活链接<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
    username, token, token)
    send_mail(subject, message, sender, receiver, html_message=html_message)


# @app.task
# def get_static_index():
#     # 获取商品的种类信息
#     types = GoodsType.objects.all()
#     # 获取首页轮播商品信息
#     goods_banners = IndexGoodsBanner.objects.all().order_by('index')
#     # 获取促销活动信息
#     goods_ptomotions = IndexPtomotionBanner.objects.all().order_by('index')
#     # 获取首页商品展示信息
#     for type in types:
#         # 获取type种类首页分类商品的图片信息
#         images_banners = IndexGoodsBanner.objects.filter(type=type, default=1).order_by('index')
#         # 获取type种类首页分类商品的文字信息
#         title_banners = IndexGoodsBanner.objects.filter(type=type, default=0).order_by('index')
#         # 动态的给type增加属性，分别保存首页分类商品的图片信息和文字信息,然后type中就有和使用images_banner和title_banner属性了
#         type.images_banners = images_banners
#         type.title_banners = title_banners
#
#     # 组织上下文
#     context = {
#         'types': types,
#         'goods_banners': goods_banners,
#         'goods_ptomotion': goods_ptomotions,
#     }
#
#     #加载模板变量
#     temp = loader.get_template('static_index.html')
#     #渲染模板
#     static_index_html = temp.render(context)
#
#     #生成首页的静态页面,在没登陆时写入
#     save_path = os.path.join(settings.BASE_DIR,'static/index.html')
#     with open(save_path,'w') as f:
#         f.write(static_index_html)