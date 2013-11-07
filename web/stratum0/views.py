from django.shortcuts import render
import cvmfs.repository

def index(request):
    stratum0_list = cvmfs.repository.all_stratum0()
    context = {'stratum0_list': stratum0_list}
    return render(request, 'stratum0/index.html', context)

def details(request, stratum1_id):
    return HttpResponse("You will look at: %s" % stratum1_id)
