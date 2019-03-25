from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.surveys18.builder.api.urls', namespace='api')),
]