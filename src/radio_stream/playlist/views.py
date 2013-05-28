from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from radio_stream.models import Played, Queue
from radio_users.models import Djs
from radio_users import retrieve_current_dj


def playlist(request):
    return queue(request)


def queue(request, user=None, page=1):
    if user is None:
        user = retrieve_current_dj()

    if user is None:
        queryset = Queue.objects.none()
    else:
        queryset = Queue.objects.all().filter(user=user)
        queryset = queryset.order_by("-time").select_related()

    paginator = Paginator(queryset, settings.RESULTS_PER_PAGE)

    try:
        page = paginator.page(int(page))
    except InvalidPage:
        raise Http404("No such page.")
    except ValueError:
        raise Http404("Invalid page number.")

    context = RequestContext(request, {
        "queue_page": page,
        "queue_user": user,
    })

    return render(request, "queue/index.html",
                  context_instance=context)


def queue_by_name(request, user, page=1):
    user = get_object_or_404(Djs, name__iexact=user)

    return queue(request, user, page)


def played(request, user=None, page=1):
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


def played_by_name(request, user, page=1):
    user = get_object_or_404(Djs, name=user)

    return played(request, user, page)
