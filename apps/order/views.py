import os
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from goods.models import DailyGoodsSKU, OrderGoodsSKU
from user.models import Address
from order.models import OrderInfo, OrderGoods
from django_redis import get_redis_connection
from django.http import JsonResponse
from datetime import datetime
from django.db import transaction       # 事务
from alipay import AliPay
from django.conf import settings
# Create your views here.


# order/place
class OrderPlace(View):
    # def get(self, request):
    #     sku_id = request.GET.get('sku_id')
    #     count = request.GET.get('count')
    #     print(sku_id)
    #
    #     user = request.user
    #
    #     # 用户检验
    #     if not user.is_authenticated:
    #         return JsonResponse({'res': 0, 'ermsg': '请先登录，再进行购买'})
    #
    #     # 参数校验
    #     if not all([sku_id, count]):
    #         return JsonResponse({'res': 1, 'ermsg': '信息不完整'})
    #
    #     # 校验商品
    #     try:
    #         sku = DailyGoodsSKU.objects.get(id=sku_id)
    #     except:
    #         return JsonResponse({'res': 2, 'ermsg': '商品不存在'})
    #
    #     # 检验数量
    #     if not int(count):
    #         return JsonResponse({'res': 3, 'ermsg': '数量无效'})
    #
    #     if int(count) > sku.stock:
    #         return JsonResponse({'res': 4, 'ermsg': '商品库存不足,余量sku.stock'})
    #
    #     # 业务处理
    #     sku.count = count
    #     sku.amount = int(count) * sku.price
    #
    #     # 获取地址
    #     address = Address.object.get(user=user)
    #
    #     # 库存更新
    #
    #     return JsonResponse({'res': 5, 'msg': '成功'})

    def post(self, request):
        # 获取用户
        user = request.user

        # 获取商品id的列表
        sku_ids = request.POST.getlist('sku_ids')

        if not all([sku_ids]):
            return redirect(reverse('cart:cart'))

        # 链接数据库
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id

        total_price = 0
        skus = []
        for sku_id in sku_ids:
            try:
                sku = DailyGoodsSKU.objects.get(id=sku_id)
                skus.append(sku)
            except:
                return redirect(reverse('cart:cart'))

            count = conn.hget(cart_key, sku_id)
            if count:
                sku.count = int(count)
                amount = sku.price * int(count)
            else:
                sku.count = 1
                amount = sku.price * 1

            sku.amount = amount
            total_price += amount

        total_count = int(conn.hlen(cart_key))
        trasit_price = 10
        total_price_num = trasit_price + total_price

        # 获取地址
        address = Address.object.filter(user=user)

        content = {
            'skus': skus,
            'total_count':total_count,
            'total_price': total_price,
            'total_price_num': total_price_num,
            'address': address,
            'sku_ids': sku_ids
        }
        return render(request, 'place-order.html', content)


# order/commit
class OrderCommit(View):
    @transaction.atomic
    def post(self, request):
        sku_ids = request.POST.get('sku_ids')
        addr_id = request.POST.get('addr_id')
        pay_method = request.POST.get('pay_method')
        tar = request.POST.get('tar')

        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 4, 'ermsg': '请先登录'})

        # 校验数据
        if not all([sku_ids, addr_id, pay_method]):
            return JsonResponse({'res': 0, 'ermsg':'信息不完整'})

        print(sku_ids)
        skus_id = []
        if not int(sku_ids):
            c = sku_ids.split("'")
            i = 1
            while True:
                try:
                    d = c[i]
                except:
                    break
                skus_id.append(c[i])
                i += 2
        else:
            skus_id.append(sku_ids)
        print(skus_id)
        print(tar)

        # 校验商品
        for sku_id in skus_id:
            if tar == '9527':
                try:
                    sku = OrderGoodsSKU.objects.get(id=sku_id)
                except:
                    return JsonResponse({'res': 1, 'ermsg': '商品不存在'})
            else:
                try:
                    sku = DailyGoodsSKU.objects.get(id=sku_id)
                except:
                    return JsonResponse({'res': 1, 'ermsg': '商品不存在'})

        # 校验地址
        try:
            address = Address.object.get(id=addr_id)
        except:
            return JsonResponse({'res': 2, 'ermsg': '地址错误'})

        # 校验支付方式
        if pay_method not in OrderInfo.PAY_METHOD_CHOICES.keys():
            # pay = OrderInfo.PAY_METHOD_CHOICES[str(pay_method)]
            return JsonResponse({'res': 3, 'ermsg': '非法支付方式'})

        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

        # total_count 和 total_price
        conn = get_redis_connection('default')
        cart_key = 'cart_%s' % user.id

        total_count = 0
        total_price = 0
        transit_price = 10

        # 设置保存点
        save_id = transaction.savepoint()

        # todo 创建OrderInfo
        if tar == '9527':
            #try:
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             address=address,
                                             pay_method=pay_method,
                                             total_price=total_price,
                                             total_count=total_count)
        else:
            # try:
            order = OrderInfo.objects.create(order_id=order_id,
                                             user=user,
                                             address=address,
                                             pay_method=pay_method,
                                             total_price=total_price,
                                             total_count=total_count,
                                             transit_price=transit_price)

        print('走了')
        print(skus_id)
        for sku_id in skus_id:
                try:
                    count = conn.hget(cart_key, sku_id)
                    count = int(count)
                except:
                    pass
                p_count = request.POST.get('count')
                print(p_count)
                if not p_count:
                    return JsonResponse({'res': 8, 'ermsg': '输入数量出错'})
                else:
                    count = int(p_count)

                print('走了')
                print(count)

                if tar == '9527':
                    try:
                        # todo 悲观锁 不给你创建order_goods的信息，直接卡在验证商品是否存在，不进行后续步骤
                        sku = OrderGoodsSKU.objects.get(id=sku_id)
                    except:
                        return JsonResponse({'res': 1, 'ermsg': '商品不存在'})
                else:
                    try:
                        # todo 悲观锁 不给你创建order_goods的信息，直接卡在验证商品是否存在，不进行后续步骤
                        sku = DailyGoodsSKU.objects.get(id=sku_id)
                    except:
                        return JsonResponse({'res': 1, 'ermsg': '商品不存在'})

                # 判断商品数量是否超出库存
                if count > sku.stock:
                    return JsonResponse({'res': 7, 'ermsg': '商品库存不足'})

                print('判断了')

                # 创建order_goods
                price = sku.price

                print(sku_ids, skus_id, addr_id, count, price)
                # todo 乐观锁, 查到了商品，但是不给创建
                    # 查商品，更新库存量
                    # DailyGoodsSKU.objects.filter(id=sku_id, stock=origin_stock).update(stock)
                    # if res == 0:
                    #      if i == 2:
                    #           transaction.savepoint_rollback(save_id)
                    #           JsonResponse({'res': , 'ermsg': '下单失败'})
                    #       continue

                if tar == '9527':
                    OrderGoods.objects.create(order=order,
                                              prev=sku,
                                              count=count,
                                              price=price
                                              )
                else:
                    OrderGoods.objects.create(order=order,
                                              sku=sku,
                                              count=count,
                                              price=price
                                              )


                # todo 更新库存量
                sku.stock -= count
                sku.sales += count
                sku.save()

                if tar == '9527':
                    transit_price = 0
                else:
                    transit_price = 10

                # todo 更新购买总数
                total_count += count
                total_price += int(count) * sku.price
                total_price += transit_price

                # todo 更新信息表的数据
                order.total_count = total_count
                order.total_price = total_price
                order.transit_price = transit_price
                order.save()

        # except:
        # 出错， 回滚到保存点
        # transaction.savepoint_rollback(save_id)
        # return JsonResponse({'res': 6, 'ermsg': '下单失败'})

        # 提交保存点，创建成功
        transaction.savepoint_commit(save_id)

        # 删除购物车中的记录
        try:
            conn.hdel(cart_key, *skus_id)           # 因为是位置参数，又是列表，进行拆包
        except:
            pass

        return JsonResponse({'res': 5, 'msg': '提交成功'})


class OrderPayView(View):
    def post(self, request):
        order_id = request.POST.get('order_id')

        user = request.user

        # 校验信息
        if not all([order_id]):
            return JsonResponse({'res': 0, 'ermsg': '信息无效'})

        # 校验订单id的有效性
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=1,
                                          order_status=1)

        except:
            return JsonResponse({'res': 1, 'ermsg': '订单信息错误'})

        # 进行业务处理，
        # 进行付款
        alipay = AliPay(
            appid="2016102200738288",
            app_notify_url=None,  # 默认回调url
            # app_private_key_string=app_private_key_string,
            app_private_key_string=open(os.path.join(settings.BASE_DIR, 'apps/order/app_private_key.pem')).read(),
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            # alipay_public_key_string=alipay_public_key_string,
            alipay_public_key_string=open(os.path.join(settings.BASE_DIR, 'apps/order/alipay_public_key.pem')).read(),
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

        # trasit_price = 10
        # 调用接口
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        total_price = order.total_price
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=str(total_price),          # 防止序列化
            subject='quickbutton%s' % order_id,
            return_url='http://127.0.0.1:8000/order/alipayback?user=%s' % user.id,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        # 返回应答
        pay_url = "https://openapi.alipaydev.com/gateway.do?" + order_string

        return JsonResponse({'res': 2, 'pay_url': pay_url})


class AlipayBackView(View):
    def get(self, request):

        out_trade_no = request.GET.get('out_trade_no')      # 订单的创建时间, 就是order_id
        total_amount = request.GET.get('total_amount')
        trade_no = request.GET.get('trade_no')

        user = request.GET.get('user')

        print(out_trade_no, total_amount, trade_no)

        if not user:
            return render(request, 'user-center-order.html', {'content': '未登录，登录信息错误'})

        if not all([out_trade_no, total_amount, trade_no]):
            return render(request, 'user-center-order.html', {'content': '信息错误'})

        if not out_trade_no:
            return render(request, 'user-center-order.html', {'content': '系统错误， 请联系客服'})

        # 查询记录
        try:
            order = OrderInfo.objects.get(order_id=out_trade_no,
                                          user=user,
                                          total_price=total_amount)
        except:
            return render(request, 'user-center-order.html', {'content': '支付信息错误， 请联系客服'})

        # 更新订单状态
        order.order_status = 4
        order.trade_no = trade_no
        order.save()

        # 返回应答
        return render(request, 'user-center-order.html', {'content': '订单完成'})


# order/comment
class OrderCommentView(View):
    def get(self, request, order_id):
        # print('获取了comment')
        user = request.user
        print(order_id)
        # 检验
        if not all([order_id]):
            return render(request, 'comment.html', {'content': '评论商品错误'})

        # 登录校验
        if not user.is_authenticated:
            render(request, 'comment.html', {'content': '请先登录再评价'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user)
            try:
                skus = OrderGoods.objects.filter(order=order)
                for sku in skus:
                    print(sku.price)
                    sku.amount = int(sku.count) * sku.price
                    print('计算了总价')

            except:
                render(request, 'comment.html', {'content': '商品不存在'})

        except:
            render(request, 'comment.html', {'content': '订单不存在'})

        return render(request, 'comment.html', {'skus': skus, 'order_id': order_id})
        # 原因是不知道找哪个模板,模板内容 分页出错

    def post(self, request, order_id):

        user = request.user

        if not user.is_authenticated:
            return render(request, 'comment.html', {'content': '请先登录再提交'})

        order_id = request.POST.get('order_id')
        tar = request.POST.get('tar')

        # 参数校验
        try:
            order_info = OrderInfo.objects.get(order_id=order_id,
                                               user=user)
        except:
            return render(request, 'comment.html', {'content': '订单不存在'})

        # 获取评价总数
        total_count = request.POST.get('total_count')
        total_count = int(total_count)

        # 获取评论
        for i in range(1, total_count+1):
            # 被评论的商品
            sku_id = request.POST.get('sku_%s' % i)

            print(tar)
            print(sku_id)
            if tar:
                try:
                    order = OrderGoodsSKU.objects.get(id=sku_id)
                    print(order)
                except:
                    return render(request, 'comment.html', {'content': '评价商品不存在'})
            else:
                try:
                    DailyGoodsSKU.objects.get(id=sku_id)
                except:
                    return render(request, 'comment.html', {'content': '评价商品不存在'})
            # 评论
            comment = request.POST.get('comment_%s' % i)

            # 更新表数据
            if tar:
                order = OrderGoods.objects.get(order_id=order_id,
                                               prev_id=sku_id)
            else:
                order = OrderGoods.objects.get(order_id=order_id,
                                               sku_id=sku_id)
            order.comment = comment
            order.observer = user.username
            order_info.order_status = 5
            print(order_info.order_status)
            order.save()
            order_info.save()

        return render(request, 'user-center-order.html', {'content': '评论成功'})