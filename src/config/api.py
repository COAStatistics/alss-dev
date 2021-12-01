from rest_framework.routers import DefaultRouter
from .views import ExportViewSet

api = DefaultRouter()
api.trailing_slash = "/?"

api.register(r"export", ExportViewSet, basename='export')
