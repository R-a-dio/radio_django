from django import forms
from django.core import exceptions
from .widgets import BitrateWidget, MusicFileWidget


class MusicFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.get('widget', MusicFileWidget)
        super(MusicFileField, self).__init__(*args, **kwargs)

class BitrateField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = kwargs.get('widget', BitrateWidget)
        super(BitrateField, self).__init__(*args, **kwargs)

