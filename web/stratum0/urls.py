from django.conf.urls import patterns, url

from stratum0 import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<stratum0_fqrn>.+)/replicate/(?P<stratum1_id>\d+)/$', views.StartSnapshotRedirectView.as_view(), name='replicate'),
    url(r'^(?P<stratum0_fqrn>.+)/$', views.details, name='details'),
)
