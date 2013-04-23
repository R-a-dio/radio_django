from django.db import models
from django.contrib.auth.models import User


class Songs(models.Model):
    """
    Table that keeps track of songs played by DJs
    """
    hash = models.CharField(unique=True, max_length=45, help_text="SHA1 hash of the metadata string.")
    metadata = models.TextField(help_text="The actual metadata send by the DJ")
    songid = models.ForeignKey('self')  

    def __unicode__(self):
        return self.hash

class Dj(models.Model):
    """
    Table that contains extra information for DJs, it is not required that
    each user account has one, it's fully optional.
    """
    name = models.CharField(max_length=45, help_text="Public name to be shown for this DJ.")
    description = models.TextField(blank=True,
                    help_text="A description to shown on the staff page.")
    visible = models.BooleanField(default=False, help_text="Visibility on the staff page.")
    priority = models.IntegerField(default=0, help_text="The number we sort by on the staff page, higher means closer to the top.")
    user = models.ForeignKey(User)


