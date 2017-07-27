from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^wish_items/create$', views.createPage),
    url(r'^create$', views.create),
    url(r'^wish_items/delete/(?P<id>\d+)$', views.deleteItem),
    url(r'^wish_items/add/(?P<id>\d+)$', views.addItem),
    url(r'^wish_items/remove/(?P<id>\d+)$', views.removeItem),
    url(r'^wish_items/(?P<id>\d+)$', views.itemPage)
]
