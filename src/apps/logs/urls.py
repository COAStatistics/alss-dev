from django.urls import path
from django.conf.urls import include

app_name = 'logs'

urlpatterns = [
    path('api/', include('apps.logs.api.urls', namespace='api')),
]