from django.conf.urls import url, patterns


urlpatterns = patterns('radio_stream.lastplayed.views',
    url(r"^$", 'index', name="lastplayed"),
    url(r"^(?P<page>\d+)/$", 'index', name="lastplayed_index_paging"),
    url(r"^(?P<user>\w+)/$", 'user_by_name', name="lastplayed_user"),
    url(r"^(?P<user>\w+)/(?P<page>\d+)/$", 'user_by_name', name="lastplayed_user_paging"),
)

