from django.conf.urls import url, patterns


urlpatterns = patterns('radio_stream.queue.views',
    url(r"^$", 'index', name="radio_queue_current"),
    url(r"^(?P<page>\d+)/$", 'index', name="radio_queue_page"),
    url(r"^(?P<user>\w+)/$", 'index', name="radio_queue_user"),
    url(r"^(?P<user>\w+)/(?P<page>\d+)/$", "index", name="radio_queue_user_page"),
)
