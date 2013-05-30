from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from endless_pagination.decorators import page_template

from radio_news.models import News


@page_template("radio/news/index_page.html")
def index(request, template="radio/news/index.html", extra_context=None):
    """
    View for the list view of news objects.
    """
    queryset = News.objects.all().order_by('-time')

    context = {
        "news_objects": queryset,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def detail(request, template="radio/news/detail.html", extra_context=None):
    """
    Returns a single news post. Should also allow commenting if enabled.
    """
    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def by_slug(request, slug):
    news_obj = get_object_or_404(News, slug__iexact=slug)

    return detail(request, extra_context={"news_object": news_obj})


def by_id(request, news_id):
    news_obj = get_object_or_404(News, pk=news_id)

    return detail(request, extra_context={"news_object": news_obj})
