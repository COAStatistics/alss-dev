from rest_framework.routers import DefaultRouter

from .views import ReviewLogViewSet

api = DefaultRouter()
api.trailing_slash = "/?"

api.register(r"reviewlog", ReviewLogViewSet)
