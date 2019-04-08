from django.urls import path
from django.urls.conf import include

app_name = "surveys18"

urlpatterns = [
    path("api/", include("apps.surveys18.builder.api.urls", namespace="api"))
]
