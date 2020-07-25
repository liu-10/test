from django.conf.urls import url, include
from cart.views import CartView, CartAddView, CartUpdateView, CartDeleteView

urlpatterns = [
    url(r'^cart$', CartView.as_view(), name='cart'),
    url(r'^add$', CartAddView.as_view(), name='add'),
    url(r'^update$', CartUpdateView.as_view(), name='update'),
    url(r'^delete$', CartDeleteView.as_view(), name='delete')
]
