from django.contrib import admin
from radio_news.models import News, NewsComment
from radio_django.admin import RadioAdmin


class NewsAdmin(RadioAdmin):
    exclude = ('poster',)
    prepopulated_fields = {'slug': ('title',)}

    auto_user_field = 'poster'


admin.site.register(News, NewsAdmin)


class NewsCommentAdmin(RadioAdmin):
    exclude = ('poster',)

    auto_user_field = 'poster'

admin.site.register(NewsComment, NewsCommentAdmin)
