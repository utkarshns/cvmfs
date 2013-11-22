from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from django.views.generic.base import RedirectView
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse_lazy

from stratum0.models import Stratum1
import cvmfs.repository

def index(request):
    stratum1_mapping = {
        stratum0: [ cvmfs.repository.RemoteRepository(stratum1.url) for stratum1 in
                    Stratum1.objects.filter(stratum0_fqrn=stratum0) ]
        for stratum0 in cvmfs.repository.all_local_stratum0()
    }
    context = { 'stratum1_mapping': stratum1_mapping }
    return render(request, 'stratum0/index.html', context)


@never_cache
def details(request, stratum0_fqrn):
    try:
        stratum0  = cvmfs.repository.LocalRepository(stratum0_fqrn)
        stratum1s = [ (stratum1, cvmfs.repository.RemoteRepository(stratum1.url)) for stratum1 in
                      Stratum1.objects.filter(stratum0_fqrn=stratum0_fqrn) ]
        context = { 'stratum0': stratum0, 'stratum1_list': stratum1s }
        return render(request, 'stratum0/details.html', context)
    except cvmfs.repository.RepositoryNotFound, e:
        raise Http404


class StartSnapshotRedirectView(RedirectView):
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
