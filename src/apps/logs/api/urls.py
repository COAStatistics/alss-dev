from django.conf.urls import url

from .views import (
    ReviewLogViewSet,
    ReviewLogUpdateAPIView,
    ReviewLogSingletonListAPIView,
)

urlpatterns = [
    url(r'^$', ReviewLogViewSet.as_view({'get': 'list'}), name='list'),
    url(r'^update/$', ReviewLogUpdateAPIView.as_view(), name='update'),
    url(r'^reviewlog/$', ReviewLogSingletonListAPIView.as_view(), name='list_singleton_reviewlog'),
]
