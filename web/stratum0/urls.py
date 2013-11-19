from django.conf.urls import patterns, url

from stratum0 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<stratum0_fqrn>.+)/$', views.details, name='details'),
    url(r'^(?P<stratum0_fqrn>.+)/replicate$', views.details, name='replicate'),
)
