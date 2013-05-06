from django.conf.urls import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from radio_django.api import container


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'radio_web.views.home', name='home'),
    url(r'^irc/', 'radio_web.views.irc', name='irc'),
    url(r'^news/', include('radio_news.urls')),
    url(r'^submit/', include('radio_collection.submit.urls')),
    url(r'^search/', include('radio_collection.search.urls')),
    #url(r'^request/', include('radio_collection.request.urls')),
    url(r'^queue/', include('radio_stream.queue.urls')),
    url(r'^lastplayed/', include('radio_stream.lastplayed.urls')),
    url(r'^staff/', include('radio_users.staff.urls')),
    url(r'^favourites/', include('radio_users.faves.urls')),
    #url(r'^stats/', include('radio_stream.stats.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(container.urls)),

    url(r'^grappelli/', include('grappelli.urls')),
)

#if settings.DEBUG:
#    from django.conf.urls.static import static
#
#    urlpatterns += staticfiles_urlpatterns()
