from django.db import models
from django.contrib.auth.models import User
from audit_log.models.managers import AuditLog
from radio_collection.models import Collection


class Djs(models.Model):
    """
    Table that contains extra information for DJs, it is not required that
    each user account has one, it's fully optional.
    """
    name = models.CharField(max_length=45, help_text="Public name to be shown for this DJ.")

    description = models.TextField(blank=True,
                                    help_text="A description to shown on the staff page.")

    visible = models.BooleanField(default=False, help_text="Visibility on the staff page.")

    priority = models.IntegerField(default=0,
                    help_text="The number we sort by on the staff page, higher means closer to the top.")

    user = models.OneToOneField(User, related_name='dj_account')

    log = AuditLog()


class Nicknames(models.Model):
    passcode = models.CharField(max_length=8, null=True,
                                help_text="A small passcode used for website/irc linking.")


class Names(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text="Name used on IRC.")

    nickname = models.ForeignKey(Nicknames)


class Faves(models.Model):
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="When was this faved.")

    song = models.ForeignKey('radio_stream.Songs', help_text="The song faved.")

    user = models.ForeignKey(Nicknames, help_text="The user that faved this.")

    class Meta:
        unique_together = ('user', 'song')


class Uploads(models.Model):
    identifier = models.CharField(max_length=120,
            help_text="A unique identifier to check against. (I.E IP Address, IRC Hostmask)")

    upload = models.ForeignKey(Collection,
            help_text="The track that got uploaded.")

    time = models.DateTimeField(auto_now_add=True,
            help_text="The time this was uploaded.")
