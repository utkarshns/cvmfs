from django.shortcuts import render
from stratum0.models import Stratum1
import cvmfs.repository

def index(request):
    stratum1_mapping = {
        stratum0: [ stratum1 for stratum1 in
                    Stratum1.objects.filter(stratum0_fqrn=stratum0) ]
        for stratum0 in cvmfs.repository.all_stratum0()
    }
    context = {'stratum1_mapping': stratum1_mapping}
    return render(request, 'stratum0/index.html', context)

def details(request, stratum1_id):
    return HttpResponse("You will look at: %s" % stratum1_id)
