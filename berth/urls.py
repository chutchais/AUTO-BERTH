from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pdf_view, name='index'),
]