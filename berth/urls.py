from django.conf.urls import url
from django.contrib import admin

from . import views
from .views import VoyDetailView,CutOffDetailView,CutOffUpdateView,CutOffCreateView,CutOffDeleteView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'voy/(?P<slug>[-\w]+)/$', VoyDetailView.as_view(), name='voy-detail'),
    url(r'cutoff/(?P<pk>\d+)/delete/$', CutOffDeleteView.as_view(), name='cutoff-delete'),
    url(r'cutoff/(?P<pk>\d+)/$', CutOffUpdateView.as_view(), name='cutoff-detail'),
    url(r'voy/(?P<slug>[-\w]+)/create/$',CutOffCreateView.as_view(),name='cutoff-create'),
    url(r'cutoff/$',views.cutoff, name='cutoff-home'),
]

admin.site.site_header = 'Auto Berth Schedule'