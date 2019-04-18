from django.urls import path
from django.conf.urls import include
from .api import api

app_name = "logs"

urlpatterns = [
    path("api/", include(api.urls)),
]
