from django.conf.urls import url, patterns


urlpatterns = patterns('radio_users.staff.views',
    url(r"^$", 'index', name="staff_index"),
    url(r"^(?P<user>\w+)/$", 'detail', name="staff_detail"),
)
