from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
from radio_stream.models import Played, Queue, Songs
from radio_stream import retrieve_current_song
from radio_users import retrieve_current_dj
from radio_news.models import News


def home(request):
    current_dj_object = retrieve_current_dj()


    news_objects = News.objects.all().order_by("-time")[:3]
    played_objects = Played.objects.all().select_related().order_by("time")[:10]
    queue_objects = Queue.objects.filter(user=current_dj_object).select_related().order_by("time")[:10]
    current_song_object = retrieve_current_song()


    context = RequestContext(request, {
            "news": news_objects,
            "played": played_objects,
            "queue": queue_objects,
            "current": current_song_object,
            "current_dj": current_dj_object,
        })
    return render(request, "home/index.html",
                  context_instance=context)

def irc(request):
    return render(request, "irc/index.html")
