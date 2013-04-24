from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from radio_collection.models import Tags, Tracks, Albums, Artists


class TrackIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)

    def get_model(self):
        return Tracks

