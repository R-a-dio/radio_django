from django.conf.urls import patterns, url


urlpatterns = patterns('radio_collection.request.views',
        url(r'^$', 'request', name='request'),
)
