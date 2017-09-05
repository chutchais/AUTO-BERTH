from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

admin.site.site_header = 'Auto Berth Schedule'