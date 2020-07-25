from django.conf.urls import url, include
from user.views import RegisterView, LoginView, CenterView, SiteView, OrderView, LogOutView, ChangeView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^login$', LoginView.as_view(), name='login'),
    url(r'^logout$', LogOutView.as_view(), name='logout'),
    url(r'^user-center-info$', CenterView.as_view(), name='user-center-info'),
    url(r'^user-info-site$', SiteView.as_view(), name='user-info-site'),
    url(r'^user-center-order/(?P<page>\d+)', OrderView.as_view(), name='user-center-order'),
    url(r'^change$', ChangeView.as_view(), name='change'),
]
