from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'radio_web.views.home', name='home'),
    #url(r'^irc/', 'radio_web.views.irc', name='irc'),
    #url(r'^submit/', include('radio_collection.submit.urls')),
    url(r'^search/', include('radio_collection.search.urls')),
    #url(r'^request/', include('radio_collection.request.urls')),
    #url(r'^queue/', include('radio_stream.queue.urls')),
    #url(r'^lastplayed/', include('radio_stream.lastplayed.urls')),
    #url(r'^staff/', include('radio_users.staff.urls')),
    #url(r'^favourites/', include('radio_users.faves.urls')),
    #url(r'^stats/', include('radio_stream.stats.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

from radio_django.api import container

urlpatterns += patterns('',
    url(r'^api/', include(container.urls))
)

# API root urls are defined here.
#urlpatterns += patterns('',
#    url(r'^api/tracks/search/', include('radio_collection.search.api_urls')),
#    url(r'^api/request/', include('radio_collection.request.api_urls')),
#    url(r'^api/queue/', include('radio_stream.queue.api_urls')),
#)
