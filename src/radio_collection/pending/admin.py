"""
Module providing the view for the pending list in the admin console.

"""
from django.contrib import admin
from django.conf.urls import url, patterns
from radio_collection.models import Pending

class PendingAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'album',
                    'uploader_comment', 'original_filename',
                    'status', 'decline_comment')
    list_editable = ('status', 'decline_comment')

    readonly_fields = ('uploader_comment', 'original_filename')

    search_fields = ('track__title', 'track__artist__name', 'track__album__name')

    class Meta:
        model = Pending

    def queryset(self, request):
        return self.model.objects.filter(status=self.model.PENDING)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        objects = self.queryset(request)

        form_set = []
        for obj in objects:
            form_set.append(PendingForm(instance=obj))

        extra_context['form_set'] = form_set

        return super(PendingAdmin, self).changelist_view(request, extra_context)


    change_list_template = 'admin/pending/change_list.html'

admin.site.register(Pending, PendingAdmin)

from django import forms
from django.forms.widgets import HiddenInput
from radio_collection.models import Tracks, Artists, Albums, Tags, Collection
from radio_collection.pending.fields import MusicFileField, BitrateField


class PendingForm(forms.Form):
    good = forms.BooleanField(help_text=u"Is this a good upload.")

    file = MusicFileField(help_text="The uploaded file.")

    original_filename = forms.CharField(help_text="The original filename of the track.")

    title = forms.CharField(help_text="The title of the track.")

    artist = forms.CharField(help_text="The artist of the track.")

    album = forms.CharField(help_text="The album of the track.")

    collection = forms.IntegerField(widget=HiddenInput)

    comment = forms.CharField(help_text="A comment given by the submitter.")

    bitrate = BitrateField(help_text="The bitrate of submitted file.")
    class Meta:
        model = Pending

    def __init__(self, instance=None, *args, **kwargs):
        
        initial = {
            'good': False,
            'file': instance.file,
            'title': instance.track,
            'artist': instance.track.artist,
            'album': instance.track.album,
            'comment': instance.uploader_comment,
            'bitrate': 0,
        }
        kwargs['initial'] = initial

        super(PendingForm, self).__init__(*args, **kwargs)

