from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from radio_stream.models import Songs
from django.db.models import signals


class SongIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, model_attr='metadata')

    def get_model(self):
        return Songs

def reindex_song(sender, instance, **kwargs):
    index = SongIndex()
    index.enqueue_save(instance)

signals.post_save.connect(reindex_song, sender=Songs)
