from django.core.paginator import Paginator, InvalidPage
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
from radio_stream.models import Queue
from radio_users import retrieve_current_dj


def index(request, user=None, page=1):
    if user is None:
        user = retrieve_current_dj()

    if user is None:
        queryset = Queue.objects.none()
    else:
        queryset = Queue.objects.all().filter(user=user).order_by("-time").select_related()

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
    
