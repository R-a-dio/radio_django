from radio_django.api import api_container
from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm
from radio_collection.models import Tracks
from django.core.paginator import Paginator, InvalidPage
from haystack.query import SearchQuerySet
import string


RESULTS_PER_PAGE = 15
punctuation_mapping = dict((ord(char), u' ') for char in string.punctuation)


class RadioSearchForm(SearchForm):
    def clean_q(self):
        """Remove the punctuation from teh query string"""
        return self.cleaned_data['q'].translate(punctuation_mapping)


class RadioSearchView(SearchView):
    def extra_context(self):
        return {"latest_additions": Tracks.objects.all().order_by('-id')[:RESULTS_PER_PAGE]}


"""
This creates a simple factory using django-haystack. It creates the search page for us.
"""
index = search_view_factory(
            view_class=RadioSearchView,
            template='search/query.html',
            form_class=RadioSearchForm,
            load_all=True,
            results_per_page=RESULTS_PER_PAGE,
        )


"""
This is the search API, it uses django-piston
"""
from piston.handler import BaseHandler
from piston.utils import rc

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
