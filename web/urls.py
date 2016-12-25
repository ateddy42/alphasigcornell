from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from main import views as mviews
from rush import views as rviews
from web import views as wviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^404$', mviews.error),
    
# login
    url(r'^accounts/login/$', wviews.login),
    url(r'^accounts/logout/$', wviews.logout),
    url(r'^accounts/pwd/$', wviews.pwd),

# brothers
    url(r'^brothers/$', wviews.brothers),
    url(r'^calendar/$', wviews.calendar),
    
# rush
    url(r'^rush/$', rviews.add_rush),
    url(r'^rush/save/$', rviews.save_rush),
    url(r'^rush/all/$', rviews.view_all),
    url(r'^rush/all/pic/$', rviews.view_all_pic),
    url(r'^rush/house/$', rviews.view_house),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/$', rviews.view_rush),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/comment/$', rviews.add_comment),
    url(r'^rush/(?P<first>[^_]+)_(?P<last>[^/]+)/event/$', rviews.add_event),
    url(r'^rush/users/$', rviews.view_users),

# home
    url(r'^members/$', mviews.members),
    url(r'^history/$', mviews.history),
    url(r'^recruitment/$', mviews.recruitment),
    url(r'^$', mviews.home),
    url(r'^robots.txt$', mviews.robots)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)