from django.contrib import admin
from radio_users.models import Djs, Nicknames, Names, Faves, Uploads
from radio_django.admin import RadioAdmin


class DjsAdmin(RadioAdmin):
    pass


admin.site.register(Djs, DjsAdmin)


class NicknameAdmin(RadioAdmin):
    pass

admin.site.register(Nicknames, NicknameAdmin)


class NamesAdmin(RadioAdmin):
    pass

admin.site.register(Names, NamesAdmin)


class FavesAdmin(RadioAdmin):
    list_filter = ('user', 'song', 'time')

admin.site.register(Faves, FavesAdmin)


class UploadsAdmin(RadioAdmin):
    list_filter = ('identifier', 'time')

admin.site.register(Uploads, UploadsAdmin)
