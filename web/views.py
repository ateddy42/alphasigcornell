from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from rush.models import Setting

DEFAULT_MEMBERS = 1 # 0 - off, 1 - on. Whether to show the member's tab of the website

# Check to see if DEFAULT_MEMBERS is in settings
try:
    u = Setting.objects.get(name="SHOW_MEMBERS")
except Setting.DoesNotExist:
    Setting(name="SHOW_MEMBERS", val=DEFAULT_MEMBERS).save()

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.GET.get('next', '/brothers/'))
    s = request.POST.get('s','')
    if not s:
        next = request.GET.get('next', '/brothers/')
        if (next == '/accounts/logout/'):
            next = '/brothers/' 
        return render(request, 'auth_login.html', {"next":next})
    # user submitted form. check valid, and log in
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    next = request.POST.get('next', '/brothers/')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(next)
    else:
        error = "Sorry, that's not a valid username or password combination"
        return render(request, 'auth_login.html', {"next":next, "error":error})

def logout(request):
    auth.logout(request)
    next = request.GET.get('next', '/brothers/')
    if (next == '/accounts/logout/'):
        next = '/brothers/'
    return render(request, 'auth_logout.html', {"next":next})

@login_required
def pwd(request):
    s = request.POST.get('s', '')
    if not s:
        return render(request, 'auth_pwd.html', {})
    old = request.POST.get('old', '')
    new = request.POST.get('new', '')
    confirm = request.POST.get('confirm', '')
    if not request.user.check_password(old):
        error = "Invalid current password"
        return render(request, 'auth_pwd.html', {"error":error})
    if not (len(new) > 0):
        error = "New password must be longer"
        return render(request, 'auth_pwd.html', {"error":error})
    if not (new == confirm):
        error = "New passwords do not match"
        return render(request, 'auth_pwd.html', {"error":error})
    request.user.set_password(new)
    request.user.save()
    # Need to authenticate user using new password
    user = auth.authenticate(username=request.user.username, password=new)
    auth.login(request, user)
    if request.user.has_usable_password():
        return render(request, 'auth_pwd.html', {"success":True})
    else:
        return render(request, 'auth_pwd.html', {"error":"FUCCCCCKKKK"})

@login_required
def brothers(request):
    return render(request, 'main_brothers.html')

@login_required
def calendar(request):
    return render(request, 'main_calendar.html')