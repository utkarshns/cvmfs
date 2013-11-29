from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.views.generic.base import RedirectView
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse_lazy
from datetime import datetime
from dateutil.tz import tzutc

from stratum0.models import Stratum0, Stratum1
import cvmfs.repository

def index(request):
    stratum0s = Stratum0.objects.all()
    context = { 'stratum0s': stratum0s }
    return render(request, 'stratum0/index.html', context)


@never_cache
def details(request, stratum0_fqrn):
    stratum0  = get_object_or_404(Stratum0, fqrn=stratum0_fqrn)
    stratum1s = Stratum1.objects.filter(stratum0=stratum0)
    context   = { 'stratum0'  : stratum0,
                  'stratum1s' : stratum1s }
    return render(request, 'stratum0/details.html', context)


@never_cache
def stratum0_details(request, stratum0_fqrn):
    stratum0 = get_object_or_404(Stratum0, fqrn=stratum0_fqrn)
    stratum1s = Stratum1.objects.filter(stratum0=stratum0)
    context  = { 'stratum0' : stratum0, 'stratum1s' : stratum1s }
    return render(request, 'stratum0/stratum0_details.json', context,
                  content_type="application/json")


@never_cache
def stratum1_details(request, stratum0_fqrn, stratum1_id):
    stratum0 = get_object_or_404(Stratum0, fqrn=stratum0_fqrn)
    stratum1 = get_object_or_404(Stratum1, pk=stratum1_id, stratum0=stratum0)
    context = { 'stratum0'     : stratum0,
                'stratum1'     : stratum1 }
    return render(request, 'stratum0/stratum1_details.json', context,
                  content_type="application/json")


class StartReplicationRedirectView(RedirectView):
    permanent=False

    def get_redirect_url(self, *args, **kwargs):
        stratum0_fqrn = kwargs['stratum0_fqrn']
        stratum1_id   = kwargs['stratum1_id']
        stratum0 = get_object_or_404(Stratum0, fqrn=stratum0_fqrn)
        stratum1 = get_object_or_404(Stratum1, pk=stratum1_id, stratum0=stratum0)
        stratum1_repo = stratum1.repository()

        if not stratum1_repo:
            raise Http404("Stratum 1 not found under %s" % stratum1.url)

        if not stratum1_repo.has_rest_api():
            raise Http404("Stratum 1 does not provide a REST API")

        if stratum1_repo.type != 'stratum1':
            raise Http404("%s is not a Stratum 1" % stratum1.name)

        stratum1_repo.start_replication()
        return reverse_lazy('details', kwargs={'stratum0_fqrn': stratum0.fqrn},
                            current_app='stratum0')
