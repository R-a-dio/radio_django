from django.conf.urls import patterns, url

urlpatterns = patterns('radio_collection.submit.views',
        url(r'^$', 'upload', name='submit_index'),
)
