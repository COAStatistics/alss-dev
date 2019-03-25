from django.urls import path

from .views import BuilderFileCreateAPIView

app_name = 'surveys18'

urlpatterns = [
    path('create/', BuilderFileCreateAPIView.as_view(), name='create'),
]