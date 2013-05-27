from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from radio_users.models import Djs


def index(request, template="radio/staff/index.html", extra_context=None):
    users = Djs.objects.all().filter(visible=True)

    context = {
        "user_objects": users,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def detail(request, user,
           template="radio/staff/detail.html", extra_context=None):
    user = get_object_or_404(Djs, name__iexact=user)

    context = {
        "user_object": user,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))
