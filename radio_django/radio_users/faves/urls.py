from django.conf.urls import url, patterns


urlpatterns = patterns('radio_users.faves.views',
    url(r"^$", 'index', name='radio-faves'),
    url(r"^(?P<user>[^/]+)/$", 'list_user', name="radio-faves-user"),
)
