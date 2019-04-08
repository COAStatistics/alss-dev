from django.urls import path

from .views import (
    ReviewLogViewSet,
    ReviewLogUpdateAPIView,
    ReviewLogSingletonListAPIView,
)

app_name = "logs"

urlpatterns = [
    path("", ReviewLogViewSet.as_view({"get": "list"}), name="list"),
    path("update/", ReviewLogUpdateAPIView.as_view(), name="update"),
    path(
        "reviewlog/",
        ReviewLogSingletonListAPIView.as_view(),
        name="list_singleton_reviewlog",
    ),
]
