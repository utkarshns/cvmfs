from django.shortcuts import render
from django.http import Http404

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


def details(request, stratum0_fqrn):
    try:
        stratum0  = cvmfs.repository.LocalRepository(stratum0_fqrn)
        stratum1s = [ (stratum1, cvmfs.repository.RemoteRepository(stratum1.url)) for stratum1 in
                      Stratum1.objects.filter(stratum0_fqrn=stratum0_fqrn) ]
        context = { 'stratum0': stratum0, 'stratum1_list': stratum1s }
        return render(request, 'stratum0/details.html', context)
    except cvmfs.repository.RepositoryNotFound, e:
        raise Http404
