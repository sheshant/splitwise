from django.conf.urls import url

from accounts.views import UserAPIView, UserRudView

urlpatterns = [
    url(r'^$', UserAPIView.as_view(), name='post-listcreate'),
    url(r'^(?P<pk>\d+)/$', UserRudView.as_view(), name='post-rud')
]
