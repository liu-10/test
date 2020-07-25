from django.conf.urls import url, include
from goods.views import GoodsIndex, DailyDetailView, OrderDetailView, OrderGoodsList, DailyGoodsList

urlpatterns = [
    url(r'daily-detail/(?P<gid>\d+)/(?P<page>\d+)', DailyDetailView.as_view(), name='daily-detail'),
    url(r'order-detail/(?P<gid>\d+)/(?P<page>\d+)', OrderDetailView.as_view(), name='order-detail'),
    url(r'list/(?P<type_id>\d+)/(?P<page>\d+)$', DailyGoodsList.as_view(), name='daily-list'),
    url(r'list/(?P<type_id>\d+)/(?P<num>\d+)/(?P<page>\d+)', OrderGoodsList.as_view(), name='order-list'),
    url(r'^', GoodsIndex.as_view(), name='goodsindex')
]
