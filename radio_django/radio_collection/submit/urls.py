from django.conf.urls import patterns, url


urlpatterns = patterns('radio_collection.submit.views',
    url(r'^$', 'submit_track', name='radio-submit'),
)
