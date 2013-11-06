from django.conf.urls import patterns, url

from stratum0 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
