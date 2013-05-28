from django.conf.urls import url, patterns


urlpatterns = patterns(
    'radio_stream.playlist.views',
    url(r"^$", 'playlist', name="radio-playlist"),
    url(r"^played/$", "played", name="radio-played"),
    url(r"^played/(?P<page>\d+)/$", 'played', name="radio-played-pagination"),
    url(r"^played/(?P<user>\w+)/$",
        'played_by_name',
        name="radio-played-user"),
    url(r"^played/(?P<user>\w+)/(?P<page>\d+)/$",
        'played_by_name',
        name="radio-played-user-pagination"),
    url(r"^queue/$", 'queue', name="radio-queue"),
    url(r"^queue/(?P<page>\d+)/$", 'queue', name="radio-queue-pagination"),
    url(r"^queue/(?P<user>\w+)/$", 'queue_by_name', name="radio-queue-user"),
    url(r"^queue/(?P<user>\w+)/(?P<page>\d+)/$",
        "queue_by_name",
        name="radio-queue-user-pagination"),
)
