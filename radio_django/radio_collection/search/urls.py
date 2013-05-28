from django.conf.urls import patterns, url


urlpatterns = patterns(
    'radio_collection.search.views',
    url(r'^$', 'search_index', name='radio-search'),
)
