from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^addItem$', views.addItem),
    url(r'^create$', views.create),
    url(r'^like$', views.like),
    url(r'^wish_item/(?P<id>\d+)$', views.viewItem),
    url(r'^delete$', views.delete),
    url(r'^remove$', views.remove),
    url(r'^logout$', views.logout),
    ]