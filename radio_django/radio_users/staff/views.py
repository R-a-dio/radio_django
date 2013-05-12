from django.shortcuts import render, get_object_or_404
from radio_users.models import Djs


def index(request):
    users = Djs.objects.all().filter(visible=True)

    return render(request, "radio/staff/index.html", {
        "user_objects": users,
    })

def detail(request, user):
    user = get_object_or_404(Djs, name__iexact=user)

    return render(request, "radio/staff/detail.html", {
        "user_object": user,
    })
