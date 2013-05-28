from django.conf.urls import url, patterns


urlpatterns = patterns(
    'radio_users.faves.views',
    url(r"^$", 'faves_index', name='radio-faves'),
    url(r"^(?P<user>[^/]+)/$", 'faves_list_user', name="radio-faves-user"),
)
