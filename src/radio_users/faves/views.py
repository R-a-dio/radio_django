from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from endless_pagination.decorators import page_template

from radio_users.models import Names, Faves


def faves_index(request, template="radio/faves/index.html",
                extra_context=None):

    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@page_template("radio/faves/list_page.html")
def faves_list_user(request, user,
                    template="radio/faves/list.html",
                    extra_context=None):

    name = get_object_or_404(Names, name__iexact=user)

    # We have to find all linked nicknames now
    linked_names = name.nickname.names_set.all()

    queryset = Faves.objects.filter(user__in=linked_names)

    context = {
        "fave_objects": queryset,
        "fave_user": name,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))
