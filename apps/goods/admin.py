from django.contrib import admin
from goods.models import Goods, GoodsType, GoodsImage, DailyGoodsSKU, OrderGoodsSKU, GoodsBanner
# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'detail']


class GoodsTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'logo', 'image']


class GoodsImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'daily_sku', 'order_sku', 'image']


class DailyGoodsSKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'type', 'name', 'desc', 'price',
                    'unit', 'address', 'image', 'stock', 'sales', 'status']


class OrderGoodsSKUAdmin(admin.ModelAdmin):
    list_display = ['id', 'goods', 'type', 'name', 'desc', 'price',
                    'unit', 'address', 'image', 'stock', 'sales', 'status']


class GoodsBannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'daily_sku', 'order_sku', 'display_type', 'index']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsType, GoodsTypeAdmin)
admin.site.register(GoodsImage, GoodsImageAdmin)
admin.site.register(DailyGoodsSKU, DailyGoodsSKUAdmin)
admin.site.register(OrderGoodsSKU, OrderGoodsSKUAdmin)
admin.site.register(GoodsBanner, GoodsBannerAdmin)