import re
import time
import random
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from user.models import User, Address
from django.conf import settings
from celery_tasks.tasks import send_email
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
# from django.core.cache import cache             两缓存冲突的
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMinxin
from django_redis import get_redis_connection
from goods.models import DailyGoodsSKU, OrderGoodsSKU, GoodsBanner
from order.models import OrderInfo, OrderGoods
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        is_check = request.POST.get('agree')

        print(username, password2, password, email, is_check)

        if not all([username, password, password2, email, is_check]):
            return render(request, 'register.html', {'content': '信息不完整，请重新输入'})

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            user = None
        if user:
            return render(request, 'register.html', {'content': '用户名已存在'})

        if password != password2:
            return render(request, 'register.html', {'content': '两次密码不一致'})

        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'content': '邮箱地址错误'})

        if is_check != 'on':
            return render(request, 'register.html', {'content': '请同意本协议'})

        # 进行用户注册
        register_user = User.objects.create_user(username, email, password)
        register_user.is_superuser = 0
        register_user.save()

        # 发送激活邮件
        # 发送激活链接邮件  http://127.0.0.1/user/active/5
        # 对用户信息进行加密
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'user': register_user.id}

        # 对信息进行加密
        token = serializer.dumps(info)  # byte   字节流
        token = token.decode('utf8')

        # 发送邮件
        try:
            send_email.delay(email, username, token)
        except Exception as e:
            pass
        register_user.is_active = 1
        register_user.save()

        # 重定向且反向解析到登录页面
        # return redirect(reverse('user:login'))

        # TODO:手机短信验证
        return redirect('index.html')


class LoginView(View):
    """登录视图"""
    def get(self, request):
        # 记住用户名
        if 'username' in request.COOKIES:
            is_remember = 'checked'
            username = request.COOKIES.get('username')
        else:
            is_remember = ''
            username = ''

        vcode, key = self.get_verify_code()

        self.set_key_timeout(vcode, key)

        data = {
            'vcode': vcode,
            'check': is_remember,
            'username': username
        }
        return render(request, 'login.html', data)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_vcode = request.POST.get('check-info')
        remember = request.POST.get('remember')

        # 数据检验
        if not all([username, password, check_vcode]):
            vcode, key = self.get_verify_code()
            # cache.set(key, vcode, 60)

            self.set_key_timeout(vcode, key)

            data = {
                'content': '亲，您输入信息不完整',
                'vcode': vcode
            }
            return render(request, 'login.html', data)

        # 用户不存在
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            vcode, key = self.get_verify_code()
            # cache.set(key, vcode, 60)

            self.set_key_timeout(vcode, key)

            data = {
                'content': '亲，您还未注册哦~~',
                'vcode': vcode
            }
            return render(request, 'login.html', data)

        # 用户存在
        if user:
            key = 'vcode_%s' % check_vcode

            conn = get_redis_connection('default')

            # vcode = cache.get(key)
            vcode = conn.get(key)

            if vcode:
                # 验证用户名密码
                user = authenticate(username=username, password=password)
                if user is not None:
                    # 记住登录状态
                    login(request, user)

                    # 获取未登录时跳转的页面
                    next_url = request.GET.get('next')
                    if not next_url:
                        next_url = '/'
                    # 跳转
                    response = redirect(next_url)

                    if remember == 'on':
                        response.set_cookie('username', username, max_age=7 * 24 * 3600)
                    else:
                        response.delete_cookie('username')
                    return response

                else:
                    vcode, key = self.get_verify_code()
                    # cache.set(key, vcode, 60)
                    self.set_key_timeout(vcode, key)

                    data = {
                        'content': '用户名或密码错误',
                        'vcode': vcode
                    }
                    return render(request, 'login.html', data)

            vcode, key = self.get_verify_code()

            # cache.set(key, vcode, 60)
            self.set_key_timeout(vcode, key)

            data = {
                'content': '验证码过期或错误，请重新输入',
                'vcode': vcode
            }
            return render(request, 'login.html', data)

    def get_verify_code(self):
        vcode = random.randrange(10 ** 5, 10 ** 6)
        key = 'vcode_%s' % vcode
        return vcode, key

    # 设置键的过期时间
    def set_key_timeout(self, vcode, key):
        conn = get_redis_connection('default')
        # 要在redis中有键存在，才可以设置键的过期时间
        conn.set(key, vcode)
        conn.expire(key, 120)

    # TODO 忘记密码


class LogOutView(View):
    """退出登录"""
    def get(self, request):
        logout(request)
        return redirect('/')


# user/user-center-info
class CenterView(LoginRequiredMinxin, View):
    def get(self, request):
        # 获取登录用户的实例对象
        user = request.user

        # 查看浏览记录
        # order_key = 'history_order_%s' % user.id
        key = 'history_%s' % user.id

        conn = get_redis_connection('default')
        history_list = conn.lrange(key, 0, 3)

        # 查找记录
        goods_daily = []

        for h_id in history_list:
            try:
                daily_good = DailyGoodsSKU.objects.get(id=h_id)
                print(daily_good)
                goods_daily.append(daily_good)
            except:
                pass

        # 获取地址
        address = Address.object.get_default_address(user)
        content = {
            'address': address,
            'goods_daily': goods_daily
        }
        return render(request, 'user-center-info.html', content)


# user/user-center-order
class OrderView(LoginRequiredMinxin, View):
    def get(self, request, page):
        # 获取用户
        user = request.user

        print('到了')

        # 查询所有订单id记录
        order_ids = OrderInfo.objects.filter(user=user).order_by('-create_time')

        # 遍历每一条订单id
        for order in order_ids:                     # 订单集合
            order_id = order.order_id

            # 获取每一条订单中的商品集合
            order_skus = OrderGoods.objects.filter(order_id=order_id)

            # 循环遍历动态给商品添加属性
            for order_sku in order_skus:
                # 商品小计
                if order_sku.prev:
                    amount = order_sku.prev.price * int(order_sku.count)
                    order_sku.amount = amount
                else:
                    amount = order_sku.sku.price * int(order_sku.count)
                    order_sku.amount = amount

            # 获取订单的支付状态和运费
            order_status_name = OrderInfo.ORDER_STATUS[str(order_sku.order.order_status)]

            # 添加状态中文
            order.order_status_name = order_status_name

            # 添加商品
            order.order_skus = order_skus

            # 添加状态码
            order.status_num = order_sku.order.order_status

            # 添加状态操作
            order.status_action = OrderInfo.ORDER_STATUS_ACTION[str(order_sku.order.order_status)]

        # 分页处理
        paginator = Paginator(order_ids, 5)

        # 页数校验
        try:
            page = int(page)
        except:
            page = 1

        if page > paginator.num_pages:
            page = 1

        # 获取第page页的实例对象
        page_skus = paginator.page(page)

        # 页码控制
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            range(page + 2, page + 3)

        # 组织上下文
        content = {
            'order_ids': order_ids,
            'order_skus': order_skus,
            'pages': pages,
            'page_skus': page_skus
        }
        return render(request, 'user-center-order.html', content)


# user/user-info-site
class SiteView(LoginRequiredMinxin, View):
    def get(self, request):
        # 获取登录用户的实例对象
        user = request.user

        # 获取地址
        address = Address.object.get_default_address(user)
        content = {
            'address': address
        }
        return render(request, 'user-info-site.html', content)

    def post(self, request):
        receiver = request.POST.get('receiver')
        phone = request.POST.get('phone')
        addr = request.POST.get('address')
        is_default_add = request.POST.get('is_default')

        print(receiver, phone, addr, is_default_add)

        if not all([receiver, phone, addr]):
            return render(request, 'user-info-site.html', {'content': '信息不完整'})
        else:
            if not re.match(r'1[35678]\d{9}', phone):
                return render(request, 'user-info-site.html', {'content': '手机号码错误'})

            # 获取用户实例对象
            user = request.user

            # 查看地址并判断是否为默认地址
            address = Address.object.get_default_address(user)

            if address:
                if is_default_add == 'on':
                    address.is_default = False
                    address.save()
                    print(address.is_default)
                    is_default = True
                else:
                    address.is_default = True
            else:
                is_default = True

            # 添加地址
            Address.object.create(user=user, receiver=receiver, phone=phone, is_default=is_default, address=addr)
            return redirect(reverse('user:user-info-site'))

        # TODO 编辑修改应户名和地址


# user/change
class ChangeView(View):
    def post(self, request):
        username = request.POST.get('username')
        text = request.POST.get('ch_text')
        print(text)

        user = request.user

        # 用户校验
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'ermsg': '请先登录再修改'})

        # 数据校验
        if not all([username, text]):
            return JsonResponse({'res': 1, 'ermsg': '修改信息错误'})

        # 用户名校验
        try:
            username = User.objects.get(username=username)
        except:
            return JsonResponse({'res': 2, 'ermsg': '非法用户名'})

        # 内容检验
        if not text:
            return JsonResponse({'res': 3, 'ermsg': '修改内容为空'})

        # 业务处理
        try:
            address = Address.object.get(user=username)
        except:
            return JsonResponse({'res': 4, 'ermsg': '无地址信息'})

        # 更新信息
        if re.match(r'^1[35678]\d{9}$', text):
            address.phone = text
        else:
            if re.match(r'\d+', text):
                return JsonResponse({'res': 6, 'ermsg': '非法数据,请重新修改'})
            else:
                address.address = text
        address.save()

        # 返回应答
        return JsonResponse({'res': 5, 'msg': '修改成功'})