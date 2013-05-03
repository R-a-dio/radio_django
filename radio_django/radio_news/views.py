from django.core.paginator import Paginator, InvalidPage
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from radio_news.models import News


def index(request, page=1):
    """
    View for the list view of news objects.
    """
    queryset = News.objects.all().order_by('-time')

    paginator = Paginator(queryset, settings.RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(page))
    except InvalidPage:
        raise Http404("No such page exists.")
    except ValueError:
        raise Http404("Invalid page number.")

    context = RequestContext(request, {
        "news_page": page,
    })

    return render(request, "news/index.html",
                  context_instance=context)

def detail(request, news_obj):
    """
    Returns a single news post. Should also allow commenting if enabled.
    """
    context = RequestContext(request, {
        "news_object": news_obj,
    })

    return render(request, "news/detail.html",
                  context_instance=context)


def by_slug(request, slug):
    news_obj = get_object_or_404(News, slug__iexact=slug)

    return detail(request, news_obj)

def by_id(request, news_id):
    news_obj = get_object_or_404(News, pk=news_id)

    return detail(request, news_obj)
