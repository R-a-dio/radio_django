from django.db import models
from radio_users.models import Djs
import hashlib


class Songs(models.Model):
    """
    Table that keeps track of songs played by DJs
    """
    hash = models.CharField(unique=True, max_length=45, help_text="SHA1 hash of the metadata string.")

    metadata = models.TextField(help_text="The actual metadata send by the DJ")

    songid = models.ForeignKey('self', null=True, blank=True)  

    length = models.IntegerField(help_text="The length of this song.", null=True, blank=True)

    def __unicode__(self):
        return self.hash

    @staticmethod
    def create_hash(metadata):
        if (isinstance(metadata, unicode)):
            metadata = metadata.encode('utf-8', 'replace').lower().strip()
        return hashlib.sha1(metadata).hexdigest()


class Played(models.Model):
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="The time of playing.")

    song = models.ForeignKey(Songs, help_text="The song played.")

    user = models.ForeignKey(Djs, help_text="The user that played this on stream.")


class Queue(models.Model):
    user = models.ForeignKey(Djs, help_text="The user this is queued for.")

    song = models.ForeignKey(Songs, help_text="The song queued.")

    time = models.DateTimeField(db_index=True, help_text="The estimated time of playing.")

