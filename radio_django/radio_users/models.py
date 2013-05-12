from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from radio_collection.models import Collection


class Djs(models.Model):
    """
    Table that contains extra information for DJs, it is not required that
    each user account has one, it's fully optional.
    """
    class Meta:
        verbose_name = 'dj'

    name = models.CharField(max_length=45, help_text="Public name to be shown for this DJ.")

    description = models.TextField(blank=True,
                                    help_text="A description to shown on the staff page.")

    visible = models.BooleanField(default=False, help_text="Visibility on the staff page.")

    priority = models.IntegerField(default=0,
                    help_text="The number we sort by on the staff page, higher means closer to the top.")

    user = models.OneToOneField(User, related_name='dj_account')

    image = models.ImageField(upload_to='djs/img')

    def get_absolute_url(self):
        return reverse('radio_users.staff.views.detail', kwargs={'user': self.name.lower()})

class Nicknames(models.Model):
    """
    This allows several Names to use the same passcode, each Names entry has
    one Nicknames entry as a requirement, multiple Names entries can have
    the same Nicknames entry to 'group' them together for favourites and
    other things we might implement later.
    """
    class Meta:
        verbose_name = 'nickname'

    passcode = models.CharField(max_length=8, null=True,
                                help_text="A small passcode used for website/irc linking.")


class Names(models.Model):
    """
    A Names entry is a IRC nickname, grouping is facilitated by linking to a non-unique
    Nicknames model above.
    """
    class Meta:
        verbose_name = 'name'

    name = models.CharField(max_length=30, unique=True, help_text="Name used on IRC.")

    nickname = models.ForeignKey(Nicknames)


class Faves(models.Model):
    """
    Favourites done by users in IRC, there is currently no support or plans to
    allow faveing from the website due to technical restrictions between the
    IRC protocol and the rest of our systems.
    """
    time = models.DateTimeField(null=True, blank=True, db_index=True,
                                help_text="When was this faved.")

    song = models.ForeignKey('radio_stream.Songs', help_text="The song faved.")

    user = models.ForeignKey(Names, help_text="The user that faved this.")

    class Meta:
        verbose_name = 'favourite'
        unique_together = ('user', 'song')


class Uploads(models.Model):
    """
    All known music track submissions get a corrosponding entry in this table. This is used
    for rate-limiting and as a history of any ones uploads.
    """
    class Meta:
        verbose_name = "upload"

    identifier = models.CharField(max_length=120,
            help_text="A unique identifier to check against. (I.E IP Address, IRC Hostmask)")

    upload = models.ForeignKey(Collection,
            help_text="The track that got uploaded.")

    time = models.DateTimeField(auto_now_add=True,
            help_text="The time this was uploaded.")
