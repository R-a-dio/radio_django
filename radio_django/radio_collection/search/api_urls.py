from django.conf.urls import url, patterns
from piston.resource import Resource
from radio_collection.search.views import SearchHandler

urlpatterns = patterns('',
    url(r'^$', Resource(SearchHandler)),
)
