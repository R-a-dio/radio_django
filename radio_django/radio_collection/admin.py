from django.contrib import admin
from radio_collection.models import Tracks, Collection, Artists, Albums, Tags
from radio_django.admin import RadioAdmin


class TrackAdmin(RadioAdmin):
    list_display = ('title', 'artist', 'album',)

admin.site.register(Tracks, TrackAdmin)


class ArtistAdmin(RadioAdmin):
    list_display = ('name',)

admin.site.register(Artists, ArtistAdmin)


class AlbumAdmin(RadioAdmin):
    list_display = ('name',)

admin.site.register(Albums, AlbumAdmin)


class CollectionAdmin(RadioAdmin):
    pass

admin.site.register(Collection, CollectionAdmin)


class TagsAdmin(RadioAdmin):
    list_display = ('name',)

admin.site.register(Tags, TagsAdmin)

# Add our pending admin view
import radio_collection.pending.admin
