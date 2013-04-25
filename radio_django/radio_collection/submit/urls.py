from django.conf.urls import patterns, url

urlpatterns = patterns('radio_collection.submit.views',
        url(r'^$', 'submit', name='submit_index'),
)
