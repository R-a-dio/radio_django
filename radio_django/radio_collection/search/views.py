from haystack.views import SearchView, search_view_factory
from haystack.forms import SearchForm

class RadioSearchForm(SearchForm):
    pass


RadioSearchView = SearchView


def index(request):
    """
    Index of the search page, this shows recently added songs till a search query is executed.
    """
    pass

query = search_view_factory(
            view_class=RadioSearchView,
            template='search/query.html',
            form_class=RadioSearchForm,
            load_all=True,
            results_per_page=15,
        )

def api(request):
    """
    Api access to the search engine, used by the javascript and IRC client.
    """
    pass
