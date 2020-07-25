from django.conf.urls import url, include
from order.views import OrderPlace, OrderCommit, OrderPayView, AlipayBackView, OrderCommentView

urlpatterns = [
    url(r'^place$', OrderPlace.as_view(), name='place'),
    url(r'^commit$', OrderCommit.as_view(), name='commit'),
    url(r'^pay$', OrderPayView.as_view(), name='pay'),
    url(r'^alipayback$', AlipayBackView.as_view(), name='alipayback'),
    url(r'^comment/(?P<order_id>\d+)$', OrderCommentView.as_view(), name='comment')
    # url(r'^comment$', OrderCommentView.as_view(), name='comment')
]
