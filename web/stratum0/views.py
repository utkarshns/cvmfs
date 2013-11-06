from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World!")

def details(request, stratum1_id):
    return HttpResponse("You will look at: %s" % stratum1_id)
