from django.shortcuts import render
from django.views import View
from utils.mixin import LoginRequiredMinxin
from django.http import JsonResponse
from goods.models import DailyGoodsSKU
from utils.mixin import LoginRequiredMinxin
from django_redis import get_redis_connection
# Create your views here.


# cart/cart
class CartView(LoginRequiredMinxin, View):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            conn = get_redis_connection('default')
            cart_key = 'cart_%s' % user.id
            goods = conn.hgetall(cart_key)

            skus = []
            counts = 0
            for sku_id, count in goods.items():
                sku = DailyGoodsSKU.objects.get(id=sku_id)
                sku.count = int(count)
                skus.append(sku)
                counts += 1
                price = float(sku.price)
                total_price = int(count) * price
                sku.total_price = total_price

            content = {
                'skus': skus,
                'counts': counts
            }

            return render(request, 'cart.html', content)


# cart/add
class CartAddView(View):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'ret': 0, 'ermsg': '登录后才能添加哦~'})

        # 获取ajax请求的参数
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        print(sku_id, count)

        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'ret': 1, 'ermsg': '信息不完整'})

        # 数量校验
        try:
            count = int(count)
        except:
            return JsonResponse({'ret': 2, 'ermsg': '数量输入错误'})

        # 商品校验
        try:
            sku = DailyGoodsSKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'ret': 3, 'ermsg': '商品不存在'})

        # 添加到购物车
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id

        # 查找购物车数量并更新, hget查不到返回None
        cart_count = conn.hget(cart_key, sku_id)

        if cart_count:
            count += int(cart_count)

        if count > sku.stock:
            return JsonResponse({'ret': 4, 'ermsg': '商品库存不足'})

        # hset 有就更新或没有储存
        conn.hset(cart_key, sku_id, count)
        return JsonResponse({'ret': 5, 'msg': '添加成功'})


# cart/update
class CartUpdateView(View):
    def post(self, request):
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 数据校验
        if not all([sku_id, count]):
            return JsonResponse({'res': 0, 'ermsg': '数据不完整'})

        # 商品存在校验
        try:
            sku = DailyGoodsSKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'res': 1, 'ermsg': '该商品不存在，请重新刷新'})

        # 商品数量校验
        try:
            count = int(count)
        except:
            return JsonResponse({'res': 2, 'ermsg': '数量错误'})

        if count > sku.stock:
            return JsonResponse({'res': 3, 'ermsg': '商品库存不足，余量' + str(sku.stock) })

        user = request.user
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id

        # 更新购物车的数量
        c = conn.hset(cart_key, sku_id, count)

        return JsonResponse({'res': 4, 'msg': '更新成功'})


# cart/detele
class CartDeleteView(View):
    def post(self, request):
        sku_id = request.POST.get('sku_id')

        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'ermsg': '请先登录用户'})

        # 数据校验
        if not all([sku_id]):
            return JsonResponse({'res': 1, 'ermsg': '信息错误，请重新操作'})

        # 商品校验
        try:
            sku = DailyGoodsSKU.objects.get(id=sku_id)
        except:
            return JsonResponse({'res': 2, 'ermsg': '商品不存在'})

        # 链接数据库删除数据
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id

        conn.hdel(cart_key, sku_id)

        return JsonResponse({'res': 3, 'msg': '删除成功'})
