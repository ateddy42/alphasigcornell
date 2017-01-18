from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpRequest
from rush.models import Rushee, Setting, Signin, Comment, Event, UserComment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from base64 import b64decode
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
from django.utils import timezone
import datetime

DEFAULT_QOTD = "Greatest American hero?"
TIMEOUT_VAL = 600
DEFAULT_MIRRORING = 0 # 0 - off, 1 - on
DEFAULT_COMMENTS = 1 # 0 - off, 1 - on
DEFAULT_EVENTS = 1 # 0 - off, 1 - on

# Check to see if RUSH_QOTD is in settings
try:
    u = Setting.objects.get(name="RUSH_QOTD")
except Setting.DoesNotExist:
    Setting(name="RUSH_QOTD", char=DEFAULT_QOTD).save()

# Check to see if HOUSE_MIRROR is in settings
try:
    Setting.objects.get(name="HOUSE_MIRROR")
except Setting.DoesNotExist:
    Setting(name="HOUSE_MIRROR", val=DEFAULT_MIRRORING).save()

# Check to see if HOUSE_CURRENT is in settings
try:
    Setting.objects.get(name="HOUSE_CURRENT")
except Setting.DoesNotExist:
    Setting(name="HOUSE_CURRENT").save()

# Check to see if HOUSE_TIMEOUT is in settings
try:
    Setting.objects.get(name="HOUSE_TIMEOUT")
except Setting.DoesNotExist:
    Setting(name="HOUSE_TIMEOUT", val=TIMEOUT_VAL).save()

# Check to see if RUSH_COMMENTS is in settings
try:
    u = Setting.objects.get(name="RUSH_COMMENTS")
except Setting.DoesNotExist:
    Setting(name="RUSH_COMMENTS", val=DEFAULT_COMMENTS).save()

# Check to see if RUSH_EVENTS is in settings
try:
    u = Setting.objects.get(name="RUSH_EVENTS")
except Setting.DoesNotExist:
    Setting(name="RUSH_EVENTS", val=DEFAULT_EVENTS).save()

def make_thumb(name):
    size = 120, 90
    out = settings.MEDIA_ROOT + '/rush_pics_small/' + name
    img = Image.open(settings.MEDIA_ROOT + '/rush_pics_small/' + name)
    img.thumbnail(size, Image.ANTIALIAS)
    img.save(out, "JPEG")
    return

def add_rush(request):
    s = "s" in request.GET
    e = "e" in request.GET
    qotd = Setting.objects.get(name="RUSH_QOTD").char
    return render(request, "rush_signin.html", {"s":s, "e":e, "qotd":qotd})

@login_required
def view_rush(request, first, last):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        try:
            rush = Rushee.objects.get(first=first, last=last)
            signin = rush.signin_set.order_by('date')
            comments = rush.comment_set.order_by('id')
            events = rush.event_set.order_by('event')
            comments_enabled = Setting.objects.get(name="RUSH_COMMENTS").val
            events_enabled = Setting.objects.get(name="RUSH_EVENTS").val
            try:
                thisComment = Comment.objects.get(rush=rush, user=request.user)
            except Comment.DoesNotExist:
                thisComment = ""
            can_comment = False
            try:
                can_comment = UserComment.objects.get(user=request.user).comments
            except UserComment.DoesNotExist:
                UserComment(user=request.user, comments=False).save()
            is_rush = request.user.groups.filter(name='RushChair')
            mirroring_settings = Setting.objects.get(name="HOUSE_MIRROR")
            if "m" in request.GET and is_rush: # Turn mirroring on/off
                try:
                    mirroring_settings.val = int(request.GET["m"])
                    mirroring_settings.save()
                except ValueError:
                    pass
            mirroring = mirroring_settings.val
            if "a" in request.GET and is_rush: # Make rush active/inactive
                try:
                    rush.active = int(request.GET["a"])
                    rush.save()
                    if "n" in request.GET:
                        if "va" in request.GET:
                            return HttpResponseRedirect("/rush/all/?va")
                        return HttpResponseRedirect("/rush/all/")
                except ValueError:
                    pass
            active = rush.active
            
            if is_rush and mirroring > 0:
                try:
                    r = Setting.objects.get(name="HOUSE_CURRENT")
                    r.val = rush.id
                    r.date = timezone.now()
                    r.save()
                except Setting.DoesNotExist:
                    Setting(name="HOUSE_CURRENT", val=rush.id).save()
            return render(request, "rush_single.html", {"first":first,
                                                    "last":last,
                                                    "netid":rush.netid,
                                                    "phone":rush.phone,
                                                    "build":rush.build,
                                                    "room":rush.room,
                                                    "signin":signin,
                                                    "comments":comments,
                                                    "comments_enabled":comments_enabled,
                                                    "can_comment":can_comment,
                                                    "thisComment":thisComment,
                                                    "events":events,
                                                    "events_enabled":events_enabled,
                                                    "is_rush":is_rush,
                                                    "active":active,
                                                    "mirroring":mirroring,})
        except Rushee.DoesNotExist:
            raise Http404
    else:
        return render(request, "auth_no.html")      

def view_house(request):
    mirroring = Setting.objects.get(name="HOUSE_MIRROR").val
    if mirroring == 0: # mirroring turned off
        return render(request, "rush_house.html")
    u = Setting.objects.get(name="HOUSE_CURRENT")
    comments_enabled = Setting.objects.get(name="RUSH_COMMENTS").val
    events_enabled = Setting.objects.get(name="RUSH_EVENTS").val
    d = datetime.datetime.utcnow().replace(tzinfo=None) - u.date.replace(tzinfo=None)
    if (datetime.timedelta.total_seconds(d) > Setting.objects.get(name="HOUSE_TIMEOUT").val):
        return render(request, "rush_house.html")
    try:
        rush = Rushee.objects.get(id=u.val)
        signin = rush.signin_set.order_by('date')
        comments = rush.comment_set.order_by('id')
        events = rush.event_set.order_by('event')
        return render(request, "rush_house.html", {"first":rush.first,
                                                "last":rush.last,
                                                "netid":rush.netid,
                                                "phone":rush.phone,
                                                "build":rush.build,
                                                "room":rush.room,
                                                "d":d,
                                                "comments":comments,
                                                "comments_enabled":comments_enabled,
                                                "events":events,
                                                "events_enabled":events_enabled,
                                                "signin":signin,})
    except Rushee.DoesNotExist:
        return render(request, "rush_house.html") 

@login_required
def view_all(request):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        is_rush = request.user.groups.filter(name='RushChair')
        mirroring_settings = Setting.objects.get(name="HOUSE_MIRROR")
        qotd_settings = Setting.objects.get(name="RUSH_QOTD")
        mirroring = mirroring_settings.val
        # if mirroring and not is_rush:
        #     return HttpResponseRedirect("/rush/house")
        qotd = qotd_settings.char
        if is_rush:
            if "m" in request.GET:
                try:
                    mirroring_settings.val = int(request.GET["m"])
                    mirroring_settings.save()
                except ValueError:
                    pass
                mirroring = mirroring_settings.val
            if "q" in request.GET:
                qotd = request.GET["q"]
                if len(qotd) == 0:
                    qotd = qotd_settings.char
                qotd_settings.char = qotd
                qotd_settings.save()
   
        o = "last" if not "o" in request.GET else request.GET["o"]
        rushes = []
        if "va" in request.GET:
            rushes = Rushee.objects.filter(active__gte = 0).order_by(o)
        else:
            rushes = Rushee.objects.filter(active=True).order_by(o)
        signin = Signin.objects.all()
        return render(request, "rush_all.html", {"rushes":rushes,
                                                "signin":signin,
                                                "pic":False,
                                                "is_rush":is_rush,
                                                "qotd":qotd,
                                                "va":("va" in request.GET),
                                                "mirroring":mirroring,})
    else:
        return render(request, "auth_no.html")    

@login_required
def view_all_pic(request):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        is_rush = request.user.groups.filter(name='RushChair')
        mirroring_settings = Setting.objects.get(name="HOUSE_MIRROR")
        qotd_settings = Setting.objects.get(name="RUSH_QOTD")
        mirroring = mirroring_settings.val
        # if mirroring and not is_rush:
        #     return HttpResponseRedirect("/rush/house")
        qotd = qotd_settings.char
        if is_rush:
            if "m" in request.GET:
                try:
                    mirroring_settings.val = int(request.GET["m"])
                    mirroring_settings.save()
                except ValueError:
                    pass
                mirroring = mirroring_settings.val
            if "q" in request.GET:
                qotd = request.GET["q"]
                if len(qotd) == 0:
                    qotd = qotd_settings.char
                qotd_settings.char = qotd
                qotd_settings.save()
   
        o = "last" if not "o" in request.GET else request.GET["o"]
        rushes = []
        if "va" in request.GET:
            rushes = Rushee.objects.order_by(o)
        else:
            rushes = Rushee.objects.filter(active=True).order_by(o)
        signin = Signin.objects.all()
        return render(request, "rush_all.html", {"rushes":rushes,
                                                "signin":signin,
                                                "pic":True,
                                                "is_rush":is_rush,
                                                "qotd":qotd,
                                                "va":("va" in request.GET),
                                                "mirroring":mirroring,})
    else:
        return render(request, "auth_no.html")

@login_required
def add_comment(request, first, last):
    can_view = request.user.groups.filter(name='Rush')
    comments_enabled = Setting.objects.get(name="RUSH_COMMENTS").val
    can_comment = UserComment.objects.get(user=request.user).comments
    if can_view and comments_enabled and can_comment:
        first = request.POST["first"]
        last = request.POST["last"]
        comment = request.POST["comment"]
        try:
            rush = Rushee.objects.get(first=first, last=last)
        except Rushee.DoesNotExist:
            raise Http404
        try:
            c = Comment.objects.get(rush=rush, user=request.user)
            print(comment)
            if comment == "":
                c.delete()
            else:
                c.comment = comment
                c.save()
        except Comment.DoesNotExist:
            Comment(rush=rush, comment=comment, user=request.user).save()
        return HttpResponseRedirect("/rush/" + first +"_" + last + "/")
    else:
        return HttpResponseRedirect("/rush/" + first +"_" + last + "/")

@login_required
def add_event(request, first, last):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        first = request.POST["first"]
        last = request.POST["last"]
        event = request.POST["event"]
        try:
            rush = Rushee.objects.get(first=first, last=last)
            Event(rush=rush, event=event).save()
        except Rushee.DoesNotExist:
            raise Http404
        return HttpResponseRedirect("/rush/" + first +"_" + last + "/")
    else:
        return render(request, "auth_no.html")

def save_rush(request):
    if request.POST:
        first = request.POST["first"]
        last = request.POST["last"]
        netid = request.POST["netid"]
        phone = request.POST["phone"]
        build = request.POST["build"]
        room = request.POST["room"]
        ans = request.POST["ans"]
        qotd = request.POST["qotd"]
        img = b64decode(request.POST["img"])

        if (first and last and netid and phone and build and room):
            r = 0
            try:
                r = Rushee.objects.get(first=first, last=last)
            except Rushee.DoesNotExist:
                r = Rushee(first=first, last=last, netid=netid, phone=phone, build=build, room=room)
                r.save()
            s = Signin(rush=r, qotd=qotd, ans=ans)
            if img:
                img_name = last + '-' + first + '-' + timezone.now().strftime("%d-%m-%y") + '.jpeg'
                s.img = ContentFile(img, img_name)
                s.img_small = ContentFile(img, img_name)
            else:
                img_name = 'no_img.jpeg'
            s.save()
            r.latest_signin_date = s.date
            r.save()
            if img:
                outnm = str(s.img_small).split("/")
                make_thumb(outnm[1])
                s.img_small = 'rush_pics_small/' + outnm[1]
                s.save()

        else:
            return HttpResponseRedirect("/rush/?e")
        return HttpResponseRedirect("/rush/?s")
    else:
        raise Http404

def view_users(request):
    is_rush = request.user.groups.filter(name='RushChair')
    if is_rush:
        comment_settings = Setting.objects.get(name="RUSH_COMMENTS")
        comments = comment_settings.val
        if "ec" in request.GET:
            try:
                comment_settings.val = int(request.GET["ec"])
                comment_settings.save()
                comments = comment_settings.val
            except ValueError:
                pass
        event_settings = Setting.objects.get(name="RUSH_EVENTS")
        events = event_settings.val
        if "ee" in request.GET:
            try:
                event_settings.val = int(request.GET["ee"])
                event_settings.save()
                events = event_settings.val
            except ValueError:
                pass
        if "c" in request.GET and "u" in request.GET:
            try:
                uc = UserComment.objects.get(id=int(request.GET["u"]))
                if not uc.user.groups.filter(name="RushChair"):
                    uc.comments = request.GET["c"] == '1'
                    uc.save()
            except (ValueError, User.DoesNotExist, UserComment.DoesNotExist):
                pass
        users = []
        for u in User.objects.all().order_by('last_name'):
            if not hasattr(u, 'usercomment'):
                UserComment(user = u).save()
            users.append(u.usercomment)
        return render(request, "rush_users.html", { "users":users,
                                                    "comments":comments,
                                                    "events":events,})
    else:
        return render(request, "auth_no.html")