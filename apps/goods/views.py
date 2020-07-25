from django.shortcuts import render
from django.conf import settings
from django.views import View
from goods.models import Goods, OrderGoodsSKU, DailyGoodsSKU, GoodsType, GoodsBanner
from django_redis import get_redis_connection
from django.core.paginator import Paginator
from user.models import Address
from order.models import OrderGoods
# Create your views here.


class GoodsIndex(View):
    def get(self, request):
        # 获取登录用户的实例对象
        user = request.user

        # 商品分类
        types_header = GoodsType.objects.all()
        types_daily = GoodsType.objects.all()[:5]
        types_order = GoodsType.objects.all()[5:]

        for type_daily in types_daily:
            # 获取首页的展示商品
            daily_goods = GoodsBanner.objects.filter(type=type_daily, display_type=1)
            type_daily.daily_goods = daily_goods

        for type_order in types_order:
            order_goods = GoodsBanner.objects.filter(type=type_order, display_type=1)
            type_order.order_goods = order_goods

        if user.is_authenticated:
            # 查找购物车记录
            conn = get_redis_connection('default')

            cart_key = 'cart_%s' % user.id

            cart_count = conn.hlen(cart_key)

            content = {
                'types_header': types_header,
                'types_order': types_order,
                'types_daily': types_daily,
                'cart_count': cart_count
            }
            return render(request, 'base.html', content)
        else:
            content = {
                'types_header': types_header,
                'types_order': types_order,
                'types_daily': types_daily,
            }
            return render(request, 'base.html', content)


class DailyDetailView(View):
    def get(self, request, gid, page):
        # 获取查看商品的详情
        sku = DailyGoodsSKU.objects.get(id=gid)

        # 获取新品
        news = DailyGoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 添加用户的浏览记录,浏览记录就是你只要点到了详情，系统就将记录添加到Redis去，快捷查询
        user = request.user

        # 获取地址
        address = Address.object.get(user=user)

        # 链接Redis
        conn = get_redis_connection('default')

        # 用户是否登录
        if user.is_authenticated:
            # 查找购物车数量
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

            # 查看浏览记录
            history_key = 'history_%s' % user.id
            # 有记录的话就先清空数据
            conn.lrem(history_key, 0, gid)

            # 从左侧写入数据
            conn.lpush(history_key, gid)

            # 显示几条信息
            conn.ltrim(history_key, 0, 3)

            # 获取评论
            goods = OrderGoods.objects.filter(sku_id=gid)

            print(goods)

            # 分页处理
            paginator = Paginator(list(goods), 2)

            print(paginator.num_pages)
            print(paginator.count)

            # 页数校验
            try:
                page = int(page)
            except:
                page = 1

            if page > paginator.num_pages:
                page = 1

            # 获取第page页的实例对象
            page_skus = paginator.page(page)
            print(page_skus)

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

            print(gid)
            content = {
                'sku': sku,
                'gid': gid,
                'news': news,
                'cart_count': cart_count,
                'address': address,
                'goods': goods,
                'pages': pages,
                'page_skus': page_skus
            }

            return render(request, 'daily-detail.html', content)

        return render(request, 'daily-detail.html', {'sku': sku, 'news': news})


class OrderDetailView(View):
    def get(self, request, gid, page):
        # 获取查看商品的详情
        sku = OrderGoodsSKU.objects.get(id=gid)

        # 获取新品
        news = OrderGoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 添加用户的浏览记录,浏览记录就是你只要点到了详情，系统就将记录添加到Redis去，快捷查询
        user = request.user

        # 获取地址
        address = Address.object.get(user=user)

        # 链接Redis
        conn = get_redis_connection('default')

        # 用户是否登录
        if user.is_authenticated:
            # 查找购物车数量
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            cart_count = conn.hlen(cart_key)

            # 查看浏览记录
            history_key = 'history_%s' % user.id
            # 有记录的话就先清空数据
            conn.lrem(history_key, 0, gid)

            # 从左侧写入数据
            conn.lpush(history_key, gid)

            # 显示几条信息
            conn.ltrim(history_key, 0, 4)

            # 获取评论
            comment = OrderGoods.objects.filter(prev=gid)

            # 分页处理
            paginator = Paginator(comment, 2)

            # 页码校验
            try:
                page = int(page)
            except:
                page = 1

            if page > paginator.num_pages:
                page = 1

            # 获取第page页的实例对象,便于前端用于循环
            page_skus = paginator.page(page)
            print(page_skus)

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

            content = {
                'sku': sku,
                'news': news,
                'cart_count': cart_count,
                'address': address,
                'pages': pages,
                'page_skus': page_skus,
                'gid': gid
            }

            return render(request, 'order-detail.html', content)

        return render(request, 'order-detail.html', {'sku': sku, 'news': news})


class DailyGoodsList(View):
    def get(self, request, type_id, page):

        type_all = GoodsType.objects.all()

        # 找出提交的类型
        try:
            type = GoodsType.objects.get(id=type_id)
        except:
            pass

        # 提取sort参数
        sort = request.GET.get('sort')

        if sort == 'price':
            goods = DailyGoodsSKU.objects.filter(type=type).order_by('-price')
        elif sort == 'hot':
            goods = DailyGoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            goods = DailyGoodsSKU.objects.filter(type=type).order_by('-id')

        # 获取新品
        news = DailyGoodsSKU.objects.filter(type=type_id).order_by('-create_time')[:2]

        for new in news:
            new.gd_type = 'daily-detail'

        # 获取购物车数量
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id
        cart_count = conn.hlen(cart_key)

        # 分页处理
        paginator = Paginator(goods, 2)

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

        content = {
            'cart_count': cart_count,
            'pages': pages,
            'news': news,
            'sort': sort,
            'goods': goods,
            'page_skus': page_skus,
            'type': type,
            'type_all': type_all
        }

        return render(request, 'list.html', content)


class OrderGoodsList(View):
    def get(self, request, type_id, num, page):

        type_all = GoodsType.objects.all()

        # 找出提交的类型
        try:
            type = GoodsType.objects.get(id=type_id)
        except:
            pass

        # 提取sort参数
        sort = request.GET.get('sort')

        if sort == 'price':
            goods = OrderGoodsSKU.objects.filter(type=type).order_by('-price')
        elif sort == 'hot':
            goods = OrderGoodsSKU.objects.filter(type=type).order_by('-sales')
        else:
            goods = OrderGoodsSKU.objects.filter(type=type).order_by('-id')

        # 获取新品
        news = OrderGoodsSKU.objects.filter(type=type_id).order_by('-create_time')[:2]

        good_type = {'温馨旅馆': 'order-detail'}

        for new in news:

            new.gd_type = good_type[new.type.type]

        print(new.gd_type)

        # 获取购物车数量
        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id
        cart_count = conn.hlen(cart_key)

        # 分页处理
        paginator = Paginator(goods, 2)

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

        content = {
            'cart_count': cart_count,
            'pages': pages,
            'news': news,
            'sort': sort,
            'goods': goods,
            'page_skus': page_skus,
            'type': type,
            'type_all': type_all
        }

        return render(request, 'order-list.html', content)