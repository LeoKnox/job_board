from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^board$', views.board),
    url(r'^new_job$', views.new_job),
    url(r'^create_job$', views.create_job),
]