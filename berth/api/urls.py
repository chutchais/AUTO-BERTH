from django.conf.urls import url
from django.contrib import admin

from .views import (
    VoyListAPIView,
    VoyDetailAPIView
    )

urlpatterns = [
	url(r'^$', VoyListAPIView.as_view(), name='voy_list'),
	url(r'^(?P<number>[\w-]+)/$', VoyDetailAPIView.as_view(), name='voy_detail'),
 #    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]