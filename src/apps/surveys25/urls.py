from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2025Index

app_name = "surveys25"

urlpatterns = [
    path("", Surveys2025Index.as_view(), name="surveys25_index"),
    path("api/", include(api.urls)),
]
