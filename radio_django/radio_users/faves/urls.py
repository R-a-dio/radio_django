from django.conf.urls import url, patterns


urlpatterns = patterns('radio_users.faves.views',
    url(r"^$", 'index', name='favourite_index'),
    url(r"^(?P<user>[^/]+)/$", 'list_user', name="favourite_user_list"),
)
