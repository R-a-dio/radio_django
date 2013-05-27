from django.template import RequestContext
from django.shortcuts import render_to_response

from radio_stream.models import Played, Queue
from radio_stream import retrieve_current_song
from radio_users import retrieve_current_dj
from radio_news.models import News


def home(request, template="radio/home/index.html", extra_context=None):
    current_dj_object = retrieve_current_dj()
    current_song_object = retrieve_current_song()

    news_objects = News.objects.all().order_by("-time")[:3]

    played_objects = Played.objects.all().select_related()
    played_objects = played_objects.order_by("time")[:10]

    queue_objects = Queue.objects.filter(user=current_dj_object)
    queue_objects = queue_objects.select_related().order_by('time')[:10]

    context = {
        "news": news_objects,
        "played": played_objects,
        "queue": queue_objects,
        "current": current_song_object,
        "current_dj": current_dj_object,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def irc(request, template="radio/irc/index.html", extra_context=None):
    context = {}

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))
