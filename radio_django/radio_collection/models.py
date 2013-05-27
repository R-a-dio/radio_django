from django.db import models
from django.contrib.auth.models import User
from radio_collection.utils import generate_music_filename_field


class Collection(models.Model):
    """
    A table that keeps track of our collection state. This enables us to get
    a good glance of our collection.
    """
    class Meta:
        verbose_name = u"collection information"
        verbose_name_plural = u"collection information"

    PENDING = 0
    ACCEPTED = 1
    DECLINED = 2
    REPLACEMENT = 3
    UNPLAYABLE = 4
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declinded'),
        (REPLACEMENT, 'Replacement'),
        (UNPLAYABLE, 'Unplayable'),
    )

    # A set to check if we can play our entry or not
    PLAYABLE = set((ACCEPTED, REPLACEMENT))

    track = models.OneToOneField('Tracks')

    file = models.FileField(upload_to=generate_music_filename_field,
                    help_text="Filename of the track in our system")

    original_filename = models.TextField(blank=True,
                                         help_text="Original filename.")

    good = models.BooleanField(default=False,
                               help_text="Was this a good upload.")

    status = models.IntegerField(choices=STATUS_CHOICES)

    uploader_comment = models.CharField(null=True, max_length=120,
                                help_text="Comment given by the submitter.")

    decline_comment = models.CharField(null=True, max_length=120,
                                help_text="Comment of why this was declined.")

    def __unicode__(self):
        return unicode(self.track)


class Pending(Collection):
    class Meta:
        proxy = True
        verbose_name = "pending track"

    def title(self):
        return self.track.title
    title.admin_order_field = 'track__title'

    def artist(self):
        return self.track.artist.name
    artist.admin_order_field = 'track__artist__name'

    def album(self):
        return self.track.album.name
    album.admin_order_field = 'track__album__name'


class Tags(models.Model):
    class Meta:
        verbose_name = u'tag'
        verbose_name_plural = u'tags'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Tracks(models.Model):
    class Meta:
        verbose_name = u'track'
        verbose_name_plural = u'tracks'

    title = models.TextField(help_text="Title of the track.")

    length = models.IntegerField(help_text="The length of the track.")

    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this track.")

    artist = models.ForeignKey("Artists", null=True, blank=True)

    album = models.ForeignKey("Albums", null=True, blank=True)

    # Legacy fields underneath
    legacy_tags = models.TextField(
                        help_text="Legacy tags that have not been split yet.",
                    )

    @property
    def metadata(self):
        if self.artist:
            return u"{:s} - {:s}".format(self.artist.name, self.title)
        return self.title

    def __unicode__(self):
        return self.metadata

    def last_played(self):
        try:
            return self.played_set.latest("time")
        except Played.DoesNotExist:
            return None

    def last_requested(self):
        try:
            return self.requests_set.latest('time')
        except Requests.DoesNotExist:
            return None


class Artists(models.Model):
    class Meta:
        verbose_name = 'artist'

    name = models.TextField(help_text="Name of the artist.")

    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this artist.")

    def __unicode__(self):
        return self.name


class Albums(models.Model):
    class Meta:
        verbose_name = 'album'

    name = models.TextField(help_text="Name of this album.")

    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this album.")

    def __unicode__(self):
        return self.name


class Played(models.Model):
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="Time of playback start.",
                                auto_now_add=True)
    track = models.ForeignKey(Tracks, help_text="The track played.")

    user = models.ForeignKey(User,
                        help_text="The user responsible for this playback.")

    def __unicode__(self):
        return repr(self.time)


class Requests(models.Model):
    time = models.DateTimeField(db_index=True,
                                help_text="When did this get requested.")

    track = models.ForeignKey(Tracks, help_text="The track requested.")

    identifier = models.CharField(max_length=150, db_index=True,
                                  help_text="Identifier of this request,"
                                            " either an IP or Hostname.")

    def __unicode__(self):
        return repr(self.time)

