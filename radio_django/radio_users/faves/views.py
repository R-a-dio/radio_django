from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.conf import settings
from radio_users.models import Names, Faves


def index(request):
    return render(request, "faves/index.html")


def list_user(request, user):
    name = get_object_or_404(Names, name__iexact=user)

    # We have to find all linked nicknames now
    linked_names = name.nickname.names_set.all()

    queryset = Faves.objects.filter(user__in=linked_names)

    paginator = Paginator(queryset, settings.RESULTS_PER_PAGE)

    try:
        page = paginator.page(page)
    except InvalidPage:
        raise Http404("Page does not exist.")
    except ValueError:
        raise Http404("Invalid page number.")

    return render(request, "faves/list.html", {
        "fave_page": page,
        "fave_user": nickname,
    })
