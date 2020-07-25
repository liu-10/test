from django.db import models
from eb.base_model import BaseModel
from user.models import User
from goods.models import DailyGoodsSKU, OrderGoodsSKU
# Create your models here.


class OrderInfo(BaseModel):
    PAY_METHODS = (
      (1, '货到付款'),
      (2, '微信支付'),
      (3, '支付宝'),
      (4, '银联支付')
    )

    PAY_METHODS_ENUM = {
        'CASH': 1,
        'ALIPAY': 2
    }

    ORDER_STATUS_ENUM = {
        'UNPAID': 1,
        'UNSEND': 2,
        'UNCOMMENT': 3,
        'FINISH': 4
    }

    PAY_METHOD_CHOICES = {
        '1': '货到付款',
        '2': '微信支付',
        '3': '支付宝',
        '4': '银联支付'
    }

    ORDER_STATUS = {
        '1': '待支付',
        '2': '待发货',
        '3': '待收货',
        '4': '待评价',
        '5': '已完成'
    }

    ORDER_STATUS_CHOICES = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '待收货'),
        (4, '待评价'),
        (5, '已完成')
    )

    ORDER_STATUS_ACTION = {
        '1': '去付款',
        '2': '查看物流',
        '3': '查看物流',
        '4': '去评价',
        '5': '已完成'
    }

    order_id = models.CharField(max_length=128, primary_key=True, verbose_name='订单id')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    address = models.ForeignKey('user.Address', on_delete=models.CASCADE, verbose_name='地址')
    pay_method = models.SmallIntegerField(default=3, choices=PAY_METHODS, verbose_name='支付方式')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额')
    total_count = models.IntegerField(default=1, verbose_name='总数')
    transit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='运费', null=True)
    order_status = models.SmallIntegerField(default=1, choices=ORDER_STATUS_CHOICES, verbose_name='支付状态')
    trade_no = models.CharField(max_length=50, verbose_name='支付编号', null=True, blank=True)

    class Meta:
        db_table = 'qb_order_place'
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id


class OrderGoods(BaseModel):
    order = models.ForeignKey('OrderInfo', on_delete=models.CASCADE, verbose_name='关联订单')
    sku = models.ForeignKey('goods.DailyGoodsSKU', on_delete=models.CASCADE, verbose_name='关联商品', null=True)
    prev = models.ForeignKey('goods.OrderGoodsSKU', on_delete=models.CASCADE, verbose_name='关联预定商品', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    count = models.IntegerField(default=1, verbose_name='数量')
    comment = models.CharField(max_length=256, default='', verbose_name='商品评论')
    observer = models.CharField(max_length=15, verbose_name='评论者', null=True)

    class Meta:
        db_table = 'qb_place_order'
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name
