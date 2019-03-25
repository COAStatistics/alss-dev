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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import Surveys2018Index

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Surveys2018Index.as_view(), name='index'),
    url(r'^logs/', include('apps.logs.urls', namespace='logs')),
    url(r'^2018/$', Surveys2018Index.as_view(), name='surveys18_index'),
    url(r'^surveys18/', include('apps.surveys18.urls', namespace='surveys18')),
    url(r'^2019/', include('apps.surveys19.urls', namespace='surveys19')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
