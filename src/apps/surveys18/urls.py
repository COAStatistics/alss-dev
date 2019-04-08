from django.urls import path
from django.conf.urls import include

from .views import Surveys2018Index

app_name = "surveys18"

urlpatterns = [
    path("", Surveys2018Index.as_view(), name="surveys18_index"),
    path("api/", include("apps.surveys18.api.urls", namespace="api")),
    path("builder/", include("apps.surveys18.builder.urls", namespace="builder")),
]
