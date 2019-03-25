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
from apps.surveys18.views import Surveys2018Index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Surveys2018Index.as_view(), name='index'),
    path('logs/', include('apps.logs.urls', namespace='logs')),
    path('users/', include('apps.users.urls', namespace='users')),
    path('surveys18/', include('apps.surveys18.urls', namespace='surveys18')),
    path('surveys19/', include('apps.surveys19.urls', namespace='surveys19')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
