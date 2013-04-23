from django.db import models
from django.contrib.auth.models import User
from radio_users.models import Nicknames


class Songs(models.Model):
    """
    Table that keeps track of songs played by DJs
    """
    hash = models.CharField(unique=True, max_length=45, help_text="SHA1 hash of the metadata string.")

    metadata = models.TextField(help_text="The actual metadata send by the DJ")

    songid = models.ForeignKey('self')  

    def __unicode__(self):
        return self.hash


class Faves(models.Model):
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="When was this faved.")

    song = models.ForeignKey(Songs, help_text="The song faved.")

    user = models.ForeignKey(Nicknames, help_text="The user that faved this.")

    class Meta:
        unique_together = ('user', 'song')


class Plays(models.Model):
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="The time of playing.")

    song = models.ForeignKey(Songs, help_text="The song played.")

    user = models.ForeignKey(User, help_text="The user that played this on stream.")


class Queue(models.Model):
    user = models.ForeignKey(User, help_text="The user this is queued for.")

    song = models.ForeignKey(Songs, help_text="The song queued.")

    time = models.DateTimeField(db_index=True, help_text="The estimated time of playing.")

