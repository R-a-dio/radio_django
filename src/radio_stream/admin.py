from django.contrib import admin
from radio_stream.models import Songs, Played, Queue
from radio_django.admin import RadioAdmin


class SongAdmin(RadioAdmin):
    pass

admin.site.register(Songs, SongAdmin)


class PlayedAdmin(RadioAdmin):
    pass

admin.site.register(Played, PlayedAdmin)


class QueueAdmin(RadioAdmin):
    pass


admin.site.register(Queue, QueueAdmin)
