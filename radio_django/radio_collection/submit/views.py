import logging
import datetime

from django import forms
from django.forms import Form, ModelChoiceField, CharField, FileField
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.conf import settings

from radio_collection.models import Collection, Tracks, Artists, Albums
from radio_users.models import Uploads

import mutagen


logger = logging


class ReplacementChoices(ModelChoiceField):
    """
    A subclass of ModelChoiceField that gives it a queryset that lists all
    tracks marked for replacement. It also makes sure it displays the
    correct metadata on printing.
    """
    def __init__(self):
        super(ReplacementChoices, self).\
            __init__(
                required=False,
                queryset=Collection.objects.filter(
                    status=Collection.REPLACEMENT,
                ),
            )

    def label_from_instance(self, obj):
        return obj.track.metadata


class SubmissionError(Exception):
    pass


class SubmissionForm(Form):
    """
    Submission form for new tracks in the database. This is used to render
    and check submissions before accepting them into the pending process.
    """

    track = FileField()

    comment = CharField(max_length=120, required=False)

    daypass = CharField(max_length=100, required=False)

    replace = ReplacementChoices()

    def __init__(self, request, **kwargs):
        super(SubmissionForm, self).__init__(request.POST,
                                             request.FILES,
                                             **kwargs)
        self.request = request

    def submission(self):
        """
        A small wrapper around `handle_submission` that sets our `_error`
        attribute if an error is raised.
        """
        self._errors.setdefault(
            forms.forms.NON_FIELD_ERRORS,
            forms.util.ErrorList()
        )

        try:
            self.handle_submission()
        except SubmissionError as err:
            self._errors[forms.forms.NON_FIELD_ERRORS].append(unicode(err))
            logger.exception(u"Submission error")
        except Exception as err:
            message = u"Unexpected error occured: {:s}".format(err)
            self._errors[forms.forms.NON_FIELD_ERRORS].append(message)
            logger.exception(u"Unexpected error occured")

    def validate_file(self, fileobj, filename):
        """
        Validate fileobj/filename to be a valid allowed submission.

        This uses the mutagen library to parse the headers of the file, then
        checks the SUBMISSION_MAX_SIZE_MAPPING setting and makes sure the file
        is below the allowed size threshold.

        :params fileobj: A Django File object.
        :params filename: The filename of the Django File object.
        :returns: The instance returned by :func:`mutagen.File`
        """
        try:
            song_info = mutagen.File(filename, easy=True)
        except IOError as err:
            raise SubmissionError(
                "Error inspecting submitted file: {:s}".format(err)
            )

        maximum_size = settings.SUBMISSION_MAX_SIZE_MAPPING.get(
            type(song_info),
            None
        )

        if maximum_size is None:
            raise SubmissionError(u"Uploaded file is unsupported.")

        if fileobj.size > maximum_size:
            raise SubmissionError(u"Uploaded file was too large.")

        return song_info

    def authorize(self):
        """
        Check if the user is authorized to upload a track already. This works
        by using the IP address and a history of uploads to check a submission
        threshold. This is a time period that any user has to wait before they
        can submit a track again.

        The submission delay can be set by setting SUBMISSION_DELAY in the
        settings file.

        This exports the IP address from the request as :attr:`ip_address`.

        :returns: Nothing
        """
        ip_address = self.request.META.get("REMOTE_ADDR", None)

        # Check if the IP is allowed to submit already.
        if not ip_address:
            raise SubmissionError(u"You don't have an IP address.")

        submit_threshold = datetime.datetime.now() - settings.SUBMISSION_DELAY

        # Check recent uploads by the user.
        recent_upload = Uploads.objects.filter(identifier=ip_address,
                                               time__gt=submit_threshold)

        if (recent_upload and
                not self.request.user.is_authenticated() and
                not settings.DEBUG):
            raise SubmissionError(
                u"You have to wait before uploading another song."
            )

        self.ip_address = ip_address

    def handle_submission(self):
        """
        This function does all the heavy lifting for submissions.

        We don't use the validation of the Form due to our need of request
        specific information. Most notable the ip address.

        This function does the following procedures in order:
            - Make sure the user is allowed to submit by their IP address
            - Make sure the file is acceptable; This checks:
                - Filesize (by checking SUBMISSION_MAX_SIZE_MAPPING)
                - Mutagen readability
                - Enabled support (by checking SUBMISSION_MAX_SIZE_MAPPING)
            - Get or create the Artist entry.
            - Get or create the Album entry.
            - Check if we have at the very least a Title for the track.
            - Get or create the Track entry.
                - This will return an error if the track already exists.
            - Create Collection entry.
            - Create Uploads entry.
        """
        # TODO: Split this up into smaller methods.
        self.authorize()

        # Get our fileobj from the uploaded files
        song = self.files['track']

        # We need the temporary filename for mutagen to be able to open it.
        # Warning: Django does not create a temporary file for small files.
        try:
            filename = song.temporary_file_path()
        except AttributeError:
            raise SubmissionError(
                "Unexpected error occured, poke someone "
                "on IRC (error code: 4666)"
            )

        # Validate and retrieve the information from mutagen
        song_info = self.validate_file(song, filename=filename)

        # Handle the artist tags
        artist_obj = create_object_from_mutagen(song_info, 'artist',
                                                Artists, target='name')

        album_obj = create_object_from_mutagen(song_info, 'album',
                                               Albums, target='name')

        # Create a default for when we need to create an entry.
        track_defaults = {"length": int(song_info.info.length)}

        track_obj = create_object_from_mutagen(song_info,
                                               'title',
                                               Tracks,
                                               extra={
                                                   'artist': artist_obj,
                                                   'album': album_obj,
                                                   'defaults': track_defaults,
                                               })
        if not track_obj:
            raise SubmissionError(
                u"Please at least supply a track title tag."
            )

        if not track_obj.created:
            raise SubmissionError(u"Duplicate detected in the database.")

        # TODO: Add error handling?
        collection_obj = Collection.objects.create(
            track=track_obj,
            file=song,
            status=Collection.PENDING,
            uploader_comment=self.cleaned_data['comment'],
        )

        Uploads.objects.create(
            identifier=self.ip_address,
            upload=collection_obj,
            time=datetime.datetime.now()
        )


def submit_track(request, template="radio/submit/index.html",
                 extra_context=None):
    if request.method == 'POST':
        form = SubmissionForm(request)
        if form.is_valid():
            form.submission()
    else:
        form = SubmissionForm()

    accepted = Collection.objects.filter(status=Collection.ACCEPTED)\
                                 .select_related()

    declined = Collection.objects.filter(status=Collection.DECLINED)\
                                 .select_related()

    context = {
        'form': form,
        'accepted': accepted,
        'declined': declined,
    }

    if extra_context is not None:
        context.update(extra_context)

    return render_to_response(template, context,
                              context_instance=RequestContext(request))


def create_object_from_mutagen(info, field, Model, extra=None, target=None):
    target = target or field

    extra = extra or {}

    obj = None

    meta = info.get(field, None)

    if not meta:
        return None

    # Mutagen returns a list with the possibility of multiple entries.
    meta = " ,".join(meta)

    kwargs = {target: meta}
    kwargs.update(extra)

    obj, created = Model.objects.get_or_create(**kwargs)
    obj.created = created

    return obj
