from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('apps.surveys18.api.urls', namespace='api')),
    url(r'^builder/', include('apps.surveys18.builder.urls', namespace='builder')),
]