from django.conf.urls import url
from django.contrib import admin

from . import views
from .views import ContainerListView,FileProcess,BayReport,BayDetail,ContainerDetailView,ContainerUpdateView,BayRestore

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'(?P<slug>[-\w]+)/$', BayReport, name='bay'), #File Slug
    url(r'(?P<slug>[-\w]+)/(?P<bay>\d+)$', BayDetail, name='detail'), #File Slug
    url(r'(?P<slug>[-\w]+)/process$', FileProcess,name='process'),
    # url(r'(?P<slug>[-\w]+)/delete$', BayPlanDeleteView.as_view(),name='delete'),
    # url(r'(?P<slug>[-\w]+)/edit$', BayPlanUpdateView.as_view(),name='edit'),
    url(r'stowage/(?P<slug>[-\w]+)/restore$', BayRestore,name='stowage-restore'), #Stowage Slug
    url(r'stowage/(?P<slug>[-\w]+)$', ContainerUpdateView.as_view(),name='stowage'), #Stowage Slug
    
    # url(r'^$', ItemListView.as_view(),name='list'),
]
