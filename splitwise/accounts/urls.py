from django.conf.urls import url

from accounts.views import UserAPIView, UserRudView, UserAddTransactionView

urlpatterns = [
    url(r'^$', UserAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', UserRudView.as_view(), name='post-rud'),
    url(r'^add_transaction/$', UserAddTransactionView.as_view(), name='add_transaction'),
]
