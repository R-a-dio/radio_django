from django.db.models import signals
from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from radio_collection.models import Tags, Tracks, Albums, Artists


class TrackIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(use_template=True, document=True)

    def get_model(self):
        return Tracks


def reindex_related(sender, instance, **kwargs):
    index = kwargs.get('track_index', TrackIndex())
    for track in instance.tracks_set.all():
        index.update_object(track)

# Register them to all our related senders
signals.post_save.connect(reindex_related, sender=Tags)
signals.post_save.connect(reindex_related, sender=Artists)
signals.post_save.connect(reindex_related, sender=Albums)


# These are the m2m relationship signals, these are.. more work
def m2m_artist(sender, instance, action, **kwargs):
    if not action.startswith('post_'):
        return

    if reverse:
        # Tags are changed. thus instance = Tags
        index = TrackIndex()
        for obj in instance.artists_set.all():
            reindex_related(sender, obj, track_index=index)
    else:
        # Artist side changed it. thus instance = Artists
        reindex_related(sender, instance)

def m2m_album(sender, instance, action, reverse, **kwargs):
    if not action.startswith('post_'):
        return

    if reverse:
        # Tags are changed, thus instance = Tags
        index = TrackIndex()
        for obj in instance.albums_set.all():
            reindex_related(sender, obj, track_index=index)
    else:
        # Artist side changed it, thus instance = Albums
        reindex_related(sender, instance)

def m2m_track(sender, instance, action, reverse, **kwargs):
    if not action.startswith('post_'):
        return

    index = TrackIndex()
    if reverse:
        # Tags are changed, thus instance = Tags
        for obj in instance.tracks_set.all():
            index.update_object(obj)
    else:
        # Track side changed it, thus instance = Tracks
        index.update_object(instance)

signals.m2m_changed.connect(m2m_artist, sender=Artists.tags.through)
signals.m2m_changed.connect(m2m_album, sender=Albums.tags.through)
signals.m2m_changed.connect(m2m_track, sender=Tracks.tags.through)
