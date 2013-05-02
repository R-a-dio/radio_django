from django.db import models
from django.contrib.auth.models import User
from audit_log.models.managers import AuditLog


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


class Names(models.Model):
    name = models.CharField(max_length=30, unique=True, help_text="Name used on IRC.")


class Nicknames(models.Model):
    passcode = models.CharField(max_length=8, null=True,
                                help_text="A small passcode used for website/irc linking.")

    names = models.ForeignKey(Names)
