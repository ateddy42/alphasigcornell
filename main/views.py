from django.shortcuts import render
from django.http import Http404, HttpResponse
from main.models import Officer, Brother
from rush.models import Setting
from datetime import date

def home(request): 
    return render(request, 'main_home.html')

def members(request):
    officers = Officer.objects.filter(displayed=True).order_by('id')
    bros = Brother.objects.filter(active=True).order_by('last')
    for b in bros:
    	b.year = str(b.year)
    return render(request, "main_members.html", {"officers":officers, "bros":bros,})

def history(request):
    return render(request, "main_history.html")

def recruitment(request):
    return render(request, "main_recruitment.html")

def error(request):
    raise Http404

def robots(request):
    return HttpResponse("User-agent: *\nDisallow:", content_type='text/plain')