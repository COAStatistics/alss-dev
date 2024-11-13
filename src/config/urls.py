"""alss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path
from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import Index, SessionTimeout, Chart
from .api import api

schema_view = get_schema_view(
    openapi.Info(
        title="農業勞動力調查平台應用程式介面",
        default_version="v1",
    ),
    public=False,  # Do not set to True
    permission_classes=(permissions.IsAuthenticated,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", Index.as_view(), name="index"),
    path("api/", include(api.urls)),
    path("logs/", include("apps.logs.urls", namespace="logs")),
    path("users/", include("apps.users.urls", namespace="users")),
    path("106/", include("apps.surveys18.urls", namespace="surveys18")),
    path("107/", include("apps.surveys19.urls", namespace="surveys19")),
    path("108/", include("apps.surveys20.urls", namespace="surveys20")),
    path("110/", include("apps.surveys22.urls", namespace="surveys22")),
    path("111/", include("apps.surveys23.urls", namespace="surveys23")),
    path("112/", include("apps.surveys24.urls", namespace="surveys24")),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"),
    path("captcha/", include("captcha.urls")),
    path("session-timeout/", SessionTimeout.as_view(), name="sessiontimeout"),
    path('charts/', Chart.as_view(), name='charts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
