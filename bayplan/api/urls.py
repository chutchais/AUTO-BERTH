from django.conf.urls import url
from django.contrib import admin

from .views import (
	BayPlanListAPIView,
	BayPlanDetailAPIView,
	BayPlanUpdateAPIView
    )

urlpatterns = [
	url(r'^$', BayPlanListAPIView.as_view(), name='bayfile_list'),
	url(r'^(?P<slug>[\w-]+)/$', BayPlanDetailAPIView.as_view(), name='bayfile_detail'),
	url(r'^(?P<slug>[\w-]+)/update/$', BayPlanUpdateAPIView.as_view(),name='update'),
 #    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]