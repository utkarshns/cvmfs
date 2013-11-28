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
    try:
        stratum0  = cvmfs.repository.LocalRepository(stratum0_fqrn)
        stratum1s = Stratum1.objects.filter(stratum0_fqrn=stratum0_fqrn)
        context   = { 'stratum0'      : stratum0,
                      'stratum1_list' : stratum1s }
        return render(request, 'stratum0/details.html', context)
    except cvmfs.repository.RepositoryNotFound, e:
        raise Http404


@never_cache
def stratum0_details(request, stratum0_fqrn):
    try:
        stratum0 = cvmfs.repository.LocalRepository(stratum0_fqrn)
        context  = { 'stratum0' : stratum0 }
        return render(request, 'stratum0/stratum0_details.json', context,
                      content_type="application/json")
    except cvmfs.repository.RepositoryNotFound, e:
        raise Http404


@never_cache
def stratum1_details(request, stratum0_fqrn, stratum1_id):
    stratum0 = None
    try:
        stratum0 = cvmfs.repository.LocalRepository(stratum0_fqrn)
    except cvmfs.repository.RepositoryNotFound, e:
        raise Http404
    s1_ref = get_object_or_404(Stratum1, pk=stratum1_id)
    if s1_ref.stratum0_fqrn != stratum0.fqrn:
        raise Http404
    try:
        stratum1 = cvmfs.repository.RemoteRepository(s1_ref.url)
        context = { 'stratum0'     : stratum0,
                    'stratum1'     : stratum1,
                    'stratum1_ref' : s1_ref }
        return render(request, 'stratum0/stratum1_details.json', context,
                      content_type="application/json")
    except cvmfs.repository.RepositoryNotFound, e:
        context = { 'stratum0_fqrn': stratum0_fqrn, 'stratum1_id': stratum1_id }
        return render(request, 'stratum0/stratum1_not_found.json', context,
                      content_type="application/json")


class StartReplicationRedirectView(RedirectView):
    permanent=False

    def get_redirect_url(self, *args, **kwargs):
        stratum0_fqrn = kwargs['stratum0_fqrn']
        stratum1_id   = kwargs['stratum1_id']
        stratum1_info = get_object_or_404(Stratum1, pk=stratum1_id)

        if stratum1_info.stratum0_fqrn != stratum0_fqrn:
            raise Http404("FQRNs differ (%s : %s)" % (stratum1_info.stratum0_fqrn,
                                                      stratum0_fqrn))

        stratum1 = cvmfs.repository.RemoteRepository(stratum1_info.url)
        if not stratum1.has_rest_api():
            raise Http404("Stratum 1 at %s does not provide a REST API" % stratum1_info.url)

        if stratum1.type != 'stratum1':
            raise Http404("%s is not a Stratum 1" % stratum1_info.url)

        stratum1.start_replication()
        return reverse_lazy('details', kwargs={'stratum0_fqrn': stratum0_fqrn},
                            current_app='stratum0')
