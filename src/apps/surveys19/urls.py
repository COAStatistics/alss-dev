from django.urls import path
from django.conf.urls import include
from .api import api

from .views import Surveys2019Index

app_name = "surveys19"

urlpatterns = [
    path("", Surveys2019Index.as_view(), name="surveys19_index"),
    path("api/", include(api.urls)),
]
