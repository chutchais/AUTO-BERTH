"""autoberth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'^/', include('berth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(),name='login'),
    url(r'^berth/', include('berth.urls', namespace='berth')),
    url(r'^bayplan/', include('bayplan.urls', namespace='bayplan')),
    url(r'^container/', include('container.urls', namespace='container')),
    url(r'api/voy/', include("berth.api.urls", namespace='voy-api')),
    url(r'api/vessel/', include("vessel.api.urls", namespace='vessel-api')),
    url(r'api/bayplan/', include("bayplan.api.urls", namespace='bayplan-api')),
    url(r'api/container/', include("container.api.urls", namespace='container-api')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
