from django import forms
from django.forms import Form, ModelChoiceField, CharField, FileField
from django.template import RequestContext
from django.shortcuts import render
from django.conf import settings
from radio_collection.models import Collection, Tracks, Artists, Albums
from radio_users.models import Uploads
import datetime
import string
import random
import mutagen


class ReplacementChoices(ModelChoiceField):
    """
    A subclass of ModelChoiceField that gives it a queryset that lists all
    tracks marked for replacement. It also makes sure it displays the
    correct metadata on printing.
    """
    def __init__(self):
        super(ReplacementChoices, self).__init__(required=False,
                queryset=Collection.objects.filter(status=Collection.REPLACEMENT))

    def label_from_instance(self, obj):
        return obj.track.metadata

class SubmissionError(Exception):
    pass

class SubmissionForm(Form):
    """
    Submission form for new tracks in the database. This is used to render and check
    submissions before accepting them into the pending process.
    """

    track = FileField()

    comment = CharField(max_length=120, required=False)

    daypass = CharField(max_length=100, required=False)

    replace = ReplacementChoices()

    def submission(self, request):
        """
        A small wrapper around `handle_submission` that sets our `_error` attribute
        if an error is raised.
        """
        print dir(self)
        self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
        try:
            self.handle_submission(request)
        except SubmissionError as err:
            self._errors[forms.forms.NON_FIELD_ERRORS].append(err.message)
        except Exception as err:
            print err
            self._errors[forms.forms.NON_FIELD_ERRORS].append("Unexpected error occured")

    def handle_submission(self, request):
        """
        This function does all the heavy lifting for submissions.

        We don't use the validation of the Form due to our need of request specific
        information.

        This function does the following procedures in order:
            - Make sure the user is allowed to submit by their IP address
            - Make sure the file is acceptable; This checks:
                - Filesize
                - Mutagen readability
                - Enabled support
            - Get or create the Artist entry.
            - Get or create the Album entry.
            - Check if we have at the very least a Title for the track.
            - Get or create the Track entry.
                - This will return an error if the track already exists.
            - Save the file in our SUBMISSION_FILE_LOCATION
            - Create Collection entry.
            - Create Uploads entry.
        """
        ip_address = request.META.get("REMOTE_ADDR", None)
        
        # Check if the IP is allowed to submit already.
        if not ip_address:
            raise SubmissionError(u"You don't have an IP address.")

        # TODO: Make this use a global config setting.
        submit_threshold = datetime.datetime.now() - settings.SUBMISSION_DELAY


        recent_upload = Uploads.objects.filter(identifier=ip_address, time__gt=submit_threshold)

        if recent_upload and not request.user.is_authenticated() and not settings.DEBUG:
            raise SubmissionError(u"You have to wait before uploading another song.")
        
        song = self.files['track']

        try:
            filename = song.temporary_file_path()
        except AttributeError:
            raise SubmissionError(u"Unexpected error occured, poke someone on IRC (error code: 4666)")

        # TODO: Check for exceptions...
        song_info = mutagen.File(filename, easy=True)

        print song_info

        maximum_size = settings.SUBMISSION_MAX_SIZE_MAPPING.get(type(song_info), None)

        if maximum_size is None:
            raise SubmissionError(u"Uploaded file is unsupported.")

        if song.size > maximum_size:
            raise SubmissionError(u"Uploaded file was too large.")

        # Handle the artist tags
        artist_obj = None
        artist = song_info.get('artist', None)
        if artist:
            artist = u" ,".join(artist)

            artist_obj, created = Artists.objects.get_or_create(name=artist)

        album_obj = None
        album = song_info.get('album', None)
        if album:
            album = u" ,".join(album)

            album_obj, created = Albums.objects.get_or_create(name=album)


        title = song_info.get('title', None)
        if not title:
            raise SubmissionError(u"Please at least supply a track title tag.")

        title = u" ,".join(title)

        track_defaults = {"length": int(song_info.info.length)}

        track_obj, created = Tracks.objects.get_or_create(title=title, artist=artist_obj, album=album_obj,
                                                          defaults=track_defaults)
        if not created:
            raise SubmissionError(u"Duplicate detected in the database.")


        collection_obj = Collection.objects.create(
                                track=track_obj,
                                file=song,
                                status=Collection.PENDING,
                                uploader_comment=self.cleaned_data['comment'],
                                )

        uploads_obj = Uploads.objects.create(
                              identifier=ip_address,
                              upload=collection_obj,
                              time=datetime.datetime.now()
                              )


def upload(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            form.submission(request)
    else:
        form = SubmissionForm()

    context = RequestContext(request, {
        'form': form,
    })

    return render(request, 'submit/index.html', context_instance=context)
