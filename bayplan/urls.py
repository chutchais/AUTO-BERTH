from django.conf.urls import url
from django.contrib import admin

from . import views
from .views import BayPlanCreateView,VoyDetailView,BayPlanDeleteView,BayPlanUpdateView

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'(?P<slug>[-\w]+)/$', VoyDetailView.as_view(), name='voy-detail'),
    url(r'(?P<slug>[-\w]+)/create$', BayPlanCreateView.as_view(),name='create'),
    url(r'(?P<slug>[-\w]+)/delete$', BayPlanDeleteView.as_view(),name='delete'),
    url(r'(?P<slug>[-\w]+)/edit$', BayPlanUpdateView.as_view(),name='edit'),
    url(r'(?P<slug>[-\w]+)/container$', BayPlanUpdateView.as_view(),name='container'),
    # url(r'container/(?P<pk>\d+)/$', BayPlanCreateView.as_view(),name='container'),
    # url(r'^$', ItemListView.as_view(),name='list'),
]

admin.site.site_header = 'Auto Berth Schedule'
