from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.logs.api.urls', namespace='api')),
]