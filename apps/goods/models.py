from django.db import models
from eb.base_model import BaseModel
from tinymce.models import HTMLField
# Create your models here.


class Goods(BaseModel):
    """分类商品描述"""
    name = models.CharField(max_length=20, verbose_name='商品SPU名称')
    detail = HTMLField(max_length=256, verbose_name='商品SPU描述详情')

    class Meta:
        db_table = 'qb_goods'
        verbose_name = '商品总描述'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsType(BaseModel):
    """商品的分类列表"""
    type = models.CharField(max_length=20, verbose_name='商品分类总名称')
    logo = models.CharField(max_length=120, verbose_name='标识')
    image = models.ImageField(upload_to='type', verbose_name='商品图片', blank=True)

    class Meta:
        db_table = 'qb_goods_type'
        verbose_name = '分类商品列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.type


class DailyGoodsSKU(BaseModel):
    """分类商品的详情"""
    CHOICE_STATUS = (
        (1, '上线'),
        (0, '下线')
    )
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='所属SPU')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='所属类别')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价钱')
    desc = models.CharField(max_length=128, verbose_name='商品描述')
    unit = models.CharField(max_length=10, verbose_name='单位')
    address = models.CharField(max_length=128, verbose_name='商家地址')
    image = models.ImageField(upload_to='dailygoods', blank=True, verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=CHOICE_STATUS, verbose_name='是否上线')

    class Meta:
        db_table = 'qb_daily_goods'
        verbose_name = '日常商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class OrderGoodsSKU(BaseModel):
    CHOICE_STATUS = (
        (1, '上线'),
        (0, '下线')
    )
    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name='所属SPU')
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='所属类别')
    name = models.CharField(max_length=20, verbose_name='商品名称')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='价钱')
    desc = models.CharField(max_length=128, verbose_name='商品描述')
    address = models.CharField(max_length=128, verbose_name='地址')
    unit = models.CharField(max_length=10, verbose_name='单位')
    image = models.ImageField(upload_to='dailygoods', blank=True, verbose_name='商品图片')
    stock = models.IntegerField(default=1, verbose_name='商品库存')
    sales = models.IntegerField(default=0, verbose_name='商品销量')
    status = models.SmallIntegerField(default=1, choices=CHOICE_STATUS, verbose_name='是否上线')

    class Meta:
        db_table = 'qb_order_goods'
        verbose_name = '预定商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(BaseModel):
    """商品图片"""
    daily_sku = models.ForeignKey('DailyGoodsSKU', on_delete=models.CASCADE, verbose_name='日常商品SKU', null=True)
    order_sku = models.ForeignKey('OrderGoodsSKU', on_delete=models.CASCADE, verbose_name='预定商品SKU', null=True)
    image = models.ImageField(upload_to='goods', verbose_name='图片')

    class Meta:
        db_table = 'qb_goods_image'
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name


class GoodsBanner(BaseModel):
    """首页banner图"""
    DISPLAY_TYPE_CHOICES = (
        (0, '标题'),
        (1, '图片')
    )
    type = models.ForeignKey('GoodsType', on_delete=models.CASCADE, verbose_name='商品类型')
    daily_sku = models.ForeignKey('DailyGoodsSKU', on_delete=models.CASCADE, verbose_name='日常商品SKU', null=True, blank=True)
    order_sku = models.ForeignKey('OrderGoodsSKU', on_delete=models.CASCADE, verbose_name='预定商品SKU', null=True, blank=True)
    display_type = models.SmallIntegerField(default=1, choices=DISPLAY_TYPE_CHOICES, verbose_name='展示类型')
    index = models.SmallIntegerField(default=0, verbose_name='显示顺序')

    class Meta:
        db_table = 'qb_banner_goods'
        verbose_name = '主页分类展示商品'
        verbose_name_plural = verbose_name

