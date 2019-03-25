from django.conf.urls import url

from .views import BuilderFileCreateAPIView

urlpatterns = [
    url(r'^create/$', BuilderFileCreateAPIView.as_view(), name='create'),
]