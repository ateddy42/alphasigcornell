from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from main import views as mviews
from rush import views as rviews
from web import views as wviews

admin.site.site_header = "Rockledge Admin"
admin.site.site_title = "Rockledge Admin Portal"
admin.site.index_title = "Welcome to the Rockledge Administration Portal"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^404$', mviews.error, name="404"),
    
# login
    url(r'^accounts/login/$', wviews.login, name="login"),
    url(r'^accounts/logout/$', wviews.logout, name="logout"),
    url(r'^accounts/pwd/$', wviews.pwd, name="pwd"),

# brothers
    url(r'^brothers/$', wviews.brothers, name="brothers"),
    url(r'^calendar/$', wviews.calendar, name="calendar"),
    
# rush
    url(r'^rush/$', rviews.add_rush, name="rush"),
    url(r'^rush/save/$', rviews.save_rush, name="rSave"),
    url(r'^rush/all/$', rviews.view_all, name="rAll"),
    url(r'^rush/all/pic/$', rviews.view_all_pic, name="rAllPic"),
    url(r'^rush/house/$', rviews.view_house, name="rHouse"),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/$', rviews.view_rush, name="rView"),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/comment/$', rviews.add_comment, name="rComment"),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/event/$', rviews.add_event, name="rEvent"),
    url(r'^rush/users/$', rviews.view_users, name="rUsers"),

# home
    url(r'^members/$', mviews.members, name="members"),
    url(r'^history/$', mviews.history, name="history"),
    url(r'^recruitment/$', mviews.recruitment, name="recruitment"),
    url(r'^$', mviews.home, name="home"),
    url(r'^robots.txt$', mviews.robots)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)