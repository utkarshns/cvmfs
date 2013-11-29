from django.conf.urls import patterns, url

from stratum0 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^matrix/$', views.matrix, name='matrix'),
    url(r'^(?P<stratum0_fqrn>.+)/replicate/(?P<stratum1_id>\d+)/$', views.StartReplicationRedirectView.as_view(), name='replicate'),
    url(r'^(?P<stratum0_fqrn>.+)/stratum0_details/$', views.stratum0_details, name='stratum0_details'),
    url(r'^(?P<stratum0_fqrn>.+)/stratum1_details/(?P<stratum1_id>\d+)/$', views.stratum1_details, name='stratum1_details'),
    url(r'^(?P<stratum0_fqrn>.+)/$', views.details, name='details'),
)
