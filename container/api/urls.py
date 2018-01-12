from django.conf.urls import url
from django.contrib import admin

from .views import (
	ContainerListAPIView,
	ContainerDetailAPIView
    )

urlpatterns = [
	url(r'^$', ContainerListAPIView.as_view(), name='list'),
	url(r'^(?P<slug>[\w-]+)/$', ContainerDetailAPIView.as_view(), name='detail'),
 #    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]