from django.conf.urls import url, patterns
from piston.resource import Resource
from radio_collection.search.handlers import SearchHandler

urlpatterns = patterns('',
    url(r'^$', Resource(SearchHandler)),
)
