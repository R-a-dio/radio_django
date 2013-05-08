from django.conf.urls import url, patterns


urlpatterns = patterns('radio_users.staff.views',
    url(r"^$", 'index', name="radio-staff"),
    url(r"^(?P<user>\w+)/$", 'detail', name="radio-staff-detail"),
)
