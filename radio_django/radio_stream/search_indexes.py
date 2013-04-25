from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from radio_stream.models import Songs


class SongIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='meta')

    def get_model(self):
        return Songs
