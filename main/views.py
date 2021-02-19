from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from main.models import Officer, Brother
from rush.models import Setting
from datetime import date

def home(request): 
    show_members = Setting.objects.get(name="SHOW_MEMBERS").val
    return render(request, 'main_home.html', {"show_members":show_members,})

def members(request):
    if (Setting.objects.get(name="SHOW_MEMBERS").val == 1):
        officers = Officer.objects.filter(displayed=True).order_by('order')
        bros = Brother.objects.filter(active=True).order_by('last')
        show_members = Setting.objects.get(name="SHOW_MEMBERS").val
        return render(request, "main_members.html", {"officers":officers, "bros":bros, "show_members":show_members,})
    else:
        return HttpResponseRedirect("/")

def history(request):
    show_members = Setting.objects.get(name="SHOW_MEMBERS").val
    return render(request, "main_history.html", {"show_members":show_members,})

def recruitment(request):
    show_members = Setting.objects.get(name="SHOW_MEMBERS").val
    return render(request, "main_recruitment.html", {"show_members":show_members,})

def error(request):
    raise Http404

def robots(request):
    return HttpResponse("User-agent: *\nDisallow:", content_type='text/plain')