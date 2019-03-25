from django.urls import path
from django.urls.conf import include

from .api import api

app_name = 'surveys19'

urlpatterns = [
    path('', include(api.urls)),
]
