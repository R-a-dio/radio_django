from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from radio_stream.models import Played


def index(request, user=None, page=1):
    queryset = Played.objects.all().order_by("-time")

    if not user is None:
        queryset.filter(user=user)

    paginator = Paginator(queryset, settings.RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(page))
    except InvalidPage:
        raise Http404("Page does not exist.")
    except ValueError:
        raise Http404("Invalid page number.")

    context = RequestContext(request, {
        "lastplayed_page": page,
        "lastplayed_user": user,
    })

    return render(request, "lastplayed/index.html",
                  context_instance=context)

def user_by_name(request, user, page=1):
    user = get_object_or_404(Djs, name=user)

    return index(request, user, page)

