from django.db import models
from audit_log.models.managers import AuditLog


class Collection(models.Model):
    """
    A table that keeps track of our collection state. This enables us to get a good
    glance of our collection.
    """
    # Track changes.
    log = AuditLog()


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

    track = models.ForeignKey("Tracks", unique=True)

    filename = models.TextField(blank=True, help_text="Original filename.")

    good = models.BooleanField(default=False, help_text="Was this a good upload.")

    reupload_needed = models.BooleanField(default=False, help_text="Does this need a replacement.")

    status = models.IntegerField(choices=STATUS_CHOICES)

    uploader_comment = models.CharField(null=True, max_length=120,
                                        help_text="Comment given by the submitter.")

    decline_comment = models.CharField(null=True, max_length=120,
                                       help_text="Comment of why this was declined.")


class Tags(models.Model):
    name = models.CharField(max_length=100)

    log = AuditLog()


class Tracks(models.Model):
    title = models.TextField(help_text="Title of the track.")
    length = models.IntegerField(help_text="The length of the track.")
    
    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this track.")

    artist = models.ForeignKey("Artists", null=True, blank=True)

    album = models.ForeignKey("Albums", null=True, blank=True)

    log = AuditLog()

    # Legacy fields underneath
    legacy_tags = models.TextField(help_text="Legacy tags that have not been split yet.")

class Artists(models.Model):
    name = models.TextField(help_text="Name of the artist.")
    
    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this artist.")

    log = AuditLog()


class Albums(models.Model):
    name = models.TextField(help_text="Name of this album.")

    tags = models.ManyToManyField(Tags, null=True, blank=True,
                                  help_text="Relevant tags for this album.")
    
    log = AuditLog()

