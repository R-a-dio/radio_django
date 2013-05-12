from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm
from haystack.query import RelatedSearchQuerySet, SearchQuerySet
from radio_collection.search import RESULTS_PER_PAGE
from radio_collection.models import Tracks
import string


punctuation_mapping = dict((ord(char), u' ') for char in string.punctuation)


class TrackSearchForm(SearchForm):
    def clean_q(self):
        """Remove the punctuation from teh query string"""
        return self.cleaned_data['q'].translate(punctuation_mapping)

    def search(self):
        return super(TrackSearchForm, self).search().models(Tracks)


class TrackSearchView(SearchView):
    def extra_context(self):
        return {"latest_additions": Tracks.objects.all().order_by('-id')[:RESULTS_PER_PAGE]}

sqs = SearchQuerySet().using('default')

"""
This creates a simple factory using django-haystack. It creates the search page for us.
"""
index = search_view_factory(
            view_class=TrackSearchView,
            template='search/index.html',
            form_class=TrackSearchForm,
            load_all=True,
            results_per_page=RESULTS_PER_PAGE,
            searchqueryset=sqs,
        )

