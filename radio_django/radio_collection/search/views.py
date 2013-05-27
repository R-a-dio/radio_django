import collections
import string

from endless_pagination.decorators import page_template

from haystack.views import SearchView
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

from radio_collection.search import RESULTS_PER_PAGE
from radio_collection.models import Tracks


punctuation_mapping = dict((ord(char), u' ') for char in string.punctuation)


class TrackSearchForm(SearchForm):
    def clean_q(self):
        """Remove the punctuation from teh query string"""
        return self.cleaned_data['q'].translate(punctuation_mapping)

    def search(self):
        return super(TrackSearchForm, self).search().models(Tracks)


class TrackSearchView(SearchView):
    def __init__(self, *args, **kwargs):
        self._extra_context = kwargs.pop('extra_context')
        super(TrackSearchView, self).__init__(*args, **kwargs)

    def build_page(self):
        # Overridden because we don't want to use the built-in pagination
        # options. This just simply returns the result untouched and None set
        # as the paginator.
        return None, self.results

    def extra_context(self):
        latest = Tracks.objects.all().order_by('-id')[:RESULTS_PER_PAGE]
        latest = wrap_in_object(latest)

        context = {
            "latest_additions": latest,
            "search_query": self.get_query(),
        }

        if self._extra_context is not None:
            context.update(self._extra_context)

        return context


sqs = SearchQuerySet().using('default')


@page_template("radio/search/search_page.html")
def search_index(request, template="radio/search/search.html",
                 extra_context=None):

    return TrackSearchView(
        template=template,
        form_class=TrackSearchForm,
        searchqueryset=sqs,
        extra_context=extra_context,
    )(request)


SearchResult = collections.namedtuple("SearchResult", ("object",))


def wrap_in_object(queryset):
    """
    Wraps all items returned from *queryset* into a single item tuple with one
    attribute *object*. This so random querysets are compatible with haystack
    search result querysets.
    """
    for result in queryset:
        yield SearchResult(result)
