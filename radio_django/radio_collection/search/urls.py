from django.conf.urls import patterns, url


urlpatterns = patterns('radio_collection.search.views',
        url(r'^$', 'index', name='search_index'),
)
