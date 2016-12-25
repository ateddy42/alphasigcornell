from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpRequest
from rush.models import Rushee, Settings, Signin, Comment, Event, Brothers
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from base64 import b64decode
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
import datetime

DEFAULT_QOTD = "Greatest American hero?"
TIMEOUT_VAL = 600
DEFAULT_MIRRORING = 0 # 0 - off, 1 - on
DEFAULT_COMMENTS = 1 # 0 - off, 1 - on

# Check to see if RUSH_QOTD is in settings
try:
    u = Settings.objects.get(name="RUSH_QOTD")
except Settings.DoesNotExist:
    Settings(name="RUSH_QOTD", char=DEFAULT_QOTD).save()

# Check to see if HOUSE_MIRROR is in settings
try:
    Settings.objects.get(name="HOUSE_MIRROR")
except Settings.DoesNotExist:
    Settings(name="HOUSE_MIRROR", val=DEFAULT_MIRRORING).save()

# Check to see if HOUSE_CURRENT is in settings
try:
    Settings.objects.get(name="HOUSE_CURRENT")
except Settings.DoesNotExist:
    Settings(name="HOUSE_CURRENT").save()

# Check to see if HOUSE_TIMEOUT is in settings
try:
    Settings.objects.get(name="HOUSE_TIMEOUT")
except Settings.DoesNotExist:
    Settings(name="HOUSE_TIMEOUT", val=TIMEOUT_VAL).save()

# Check to see if RUSH_COMMENTS is in settings
try:
    u = Settings.objects.get(name="RUSH_COMMENTS")
except Settings.DoesNotExist:
    Settings(name="RUSH_COMMENTS", val=DEFAULT_COMMENTS).save()

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
    qotd = Settings.objects.get(name="RUSH_QOTD").char
    return render(request, "rush_signin.html", {"s":s, "e":e, "qotd":qotd})

@login_required
def view_rush(request, first, last):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        try:
            rush = Rushee.objects.get(first=first, last=last)
            signin = Signin.objects.filter(rid=rush.id).order_by('id')
            comments = Comment.objects.filter(rid=rush.id).order_by('id')
            try:
                thisComment = Comment.objects.get(rid=rush.id, broid=request.user.id).comment
                thisComment = thisComment.split(" - ", 1)[1]
            except Comment.DoesNotExist:
                thisComment = ""
            comments_enabled = Settings.objects.get(name="RUSH_COMMENTS").val
            can_comment = False
            try:
                can_comment = Brothers.objects.get(uid=request.user.id).comments
            except Brothers.DoesNotExist:
                Brothers(uid=request.user.id, comments=False).save()
            # events = Event.objects.filter(rid=rush.id).order_by('id')
            is_rush = request.user.groups.filter(name='RushChair')
            mirroring_settings = Settings.objects.get(name="HOUSE_MIRROR")
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
                    r = Settings.objects.get(name="HOUSE_CURRENT")
                    r.val = rush.id
                    r.date = datetime.datetime.now()
                    r.save()
                except Settings.DoesNotExist:
                    Settings(name="HOUSE_CURRENT", val=rush.id).save()
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
                                                    # "events":events,
                                                    "is_rush":is_rush,
                                                    "active":active,
                                                    "mirroring":mirroring,})
        except Rushee.DoesNotExist:
            raise Http404
    else:
        return render(request, "auth_no.html")      

def view_house(request):
    mirroring = Settings.objects.get(name="HOUSE_MIRROR").val
    if mirroring == 0: # mirroring turned off
        return render(request, "rush_house.html")
    u = Settings.objects.get(name="HOUSE_CURRENT")
    comments_enabled = Settings.objects.get(name="RUSH_COMMENTS").val
    d = datetime.datetime.utcnow().replace(tzinfo=None) - u.date.replace(tzinfo=None)
    if (datetime.timedelta.total_seconds(d) > Settings.objects.get(name="HOUSE_TIMEOUT").val):
        return render(request, "rush_house.html")
    try:
        rush = Rushee.objects.get(id=u.val)
        signin = Signin.objects.filter(rid=rush.id).order_by('date')
        comments = Comment.objects.filter(rid=rush.id).order_by('id')
        events = Event.objects.filter(rid=rush.id).order_by('id')
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
                                                "signin":signin,})
    except Rushee.DoesNotExist:
        return render(request, "rush_house.html") 

@login_required
def view_all(request):
    can_view = request.user.groups.filter(name='Rush')
    if can_view:
        is_rush = request.user.groups.filter(name='RushChair')
        mirroring_settings = Settings.objects.get(name="HOUSE_MIRROR")
        qotd_settings = Settings.objects.get(name="RUSH_QOTD")
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
        mirroring_settings = Settings.objects.get(name="HOUSE_MIRROR")
        qotd_settings = Settings.objects.get(name="RUSH_QOTD")
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
    comments_enabled = Settings.objects.get(name="RUSH_COMMENTS").val
    can_comment = Brothers.objects.get(uid=request.user.id).comments
    if can_view and comments_enabled and can_comment:
        first = request.POST["first"]
        last = request.POST["last"]
        comment = request.POST["comment"]
        try:
            rush = Rushee.objects.get(first=first, last=last)
        except Rushee.DoesNotExist:
            raise Http404
        try:
            c = Comment.objects.get(rid=rush.id, broid = request.user.id)
            print(comment)
            if comment == "":
                c.delete()
            else:
                c.comment = request.user.first_name + " - " + comment
                c.save()
        except Comment.DoesNotExist:
            comment = request.user.first_name + " - " + comment
            Comment(rid=rush.id, comment=comment, broid=request.user.id).save()
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
            Event(rid=rush.id, event=event).save()
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
            rid = 0
            try:
                r = Rushee.objects.get(first=first, last=last)
                rid = r.id
            except Rushee.DoesNotExist:
                r = Rushee(first=first, last=last, netid=netid, phone=phone, build=build, room=room)
                r.save()
                rid = r.id
            s = Signin(rid=r, qotd=qotd, ans=ans)
            if img:
                img_name = last + '-' + first + '-' + datetime.datetime.now().strftime("%d-%m-%y") + '.jpeg'
                s.img = ContentFile(img, img_name)
                s.img_small = ContentFile(img, img_name)
            else:
                img_name = 'no_img.jpeg'
            s.save()
            r = Rushee.objects.get(id=rid)
            r.latest_signin = s.id
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
        comment_settings = Settings.objects.get(name="RUSH_COMMENTS")
        comments = comment_settings.val
        if "ec" in request.GET:
            try:
                comment_settings.val = int(request.GET["ec"])
                comment_settings.save()
                comments = comment_settings.val
            except ValueError:
                pass
        if "c" in request.GET and "u" in request.GET:
            try:
                user = Brothers.objects.get(uid=int(request.GET["u"]))
                if not User.objects.get(id=user.uid).groups.filter(name="RushChair"):
                    user.comments = int(request.GET["c"])
                    user.save()
            except ValueError:
                pass
        users = User.objects.raw(
            """ SELECT u.id, u.first_name as first,
                    u.last_name as last,
                    b.comments as comments,
                    EXISTS(SELECT * FROM auth_user_groups ug, auth_group g
                        WHERE g.name = 'RushChair'
                        AND ug.group_id = g.id
                        AND u.id = ug.user_id) as rushChair
                FROM auth_user u, rush_brothers b
                WHERE u.id = b.uid
                ORDER BY u.last_name ASC""")
        return render(request, "rush_users.html", { "users":users,
                                                    "comments":comments,})
    else:
        return render(request, "auth_no.html")