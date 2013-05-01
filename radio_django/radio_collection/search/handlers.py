from radio_collection.models import Tracks
from piston.handler import BaseHandler
from piston.utils import rc
from haystack.query import SearchQuerySet
from django.core.paginator import Paginator
from radio_collection.search import RESULTS_PER_PAGE


class SearchHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Tracks

    fields = ('title', 'length', 'id', ('album', ('name', 'id')), ('artist', ('name', 'id')))

    def read(self, request, id=None):
        sqs = SearchQuerySet().models(Tracks).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, RESULTS_PER_PAGE)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            return rc.NOT_FOUND

        return [result.object for result in page.object_list]
