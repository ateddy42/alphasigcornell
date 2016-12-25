from django.shortcuts import render
from django.http import Http404, HttpResponse
from main.models import Officers, Brothers
from rush.models import Settings
from datetime import date

try:
    u = Settings.objects.get(name="OFFICERS_YEAR")
except Settings.DoesNotExist:
    Settings(name="OFFICERS_YEAR", val=date.today().year).save()

def home(request): 
    return render(request, 'main_home.html')

def members(request):
    u = Settings.objects.get(name="OFFICERS_YEAR")
    officers = Officers.objects.filter(year=u.val).order_by('id')
    bros = Brothers.objects.filter(active=True).order_by('last')
    return render(request, "main_members.html", {"officers":officers, "bros":bros,})

def history(request):
    return render(request, "main_history.html")

def recruitment(request):
    return render(request, "main_recruitment.html")

def error(request):
    raise Http404

def robots(request):
    return HttpResponse("User-agent: *\nDisallow:", content_type='text/plain')