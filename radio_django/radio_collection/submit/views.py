from django.forms import Form, ModelChoiceField, CharField, FileField
from django.conf import settings
from radio_collection import Collection
from radio_users import Uploads
import datetime
import string
import random


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


def handle_submission(request, form):
    ip_address = request.META.get("REMOTE_ADDR", None)
    
    # Check if the IP is allowed to submit already.
    if not self.ip_address:
        raise SubmissionError(u"You don't have an IP address.")

    # TODO: Make this use a global config setting.
    submit_threshold = datetime.datetime.now() - settings.SUBMISSION_DELAY


    recent_upload = Uploads.objects.filter(ip=self.ip_address, time__gt=submit_threshold)

    if recent_upload and not request.user.is_authenticated():
        raise SubmissionError(u"You have to wait before uploading another song.")
    
    song = form.files['track']

    try:
        filename = song.temporary_file_path()
    except AttributeError:
        raise SubmissionError(u"Unexpected error occured, poke someone on IRC (error code: 4666)")

    song_info = mutagen.File(filename, easy=True)

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
    if not track:
        raise SubmissionError(u"Please at least supply a track title tag.")

    title = u" ,".join(title)

    track_defaults = {"length": int(song_info.info.length)}

    track_obj, created = Tracks.objects.get_or_create(title=title, artist=artist_obj, album=album_obj,
                                                      defaults=track_defaults)
    if not created:
        raise SubmissionError(u"Duplicate detected in the database.")

    collection_obj = Collection.objects.create(
                            track=track_obj,
                            filename=song.name,
                            good=False,
                            reupload_needed=False,
                            status=Collection.PENDING,
                            uploader_comment=form.cleaned_data['comment'],
                            decline_comment=None
                            )

    uploads_obj = Uploads.objects.create(
                          address=ip_address,
                          upload=collection_obj,
                          time=datetime.datetime.now()
                          )

    save_submission(song)


# This is a string of characters we use for filename generation, this should really
# not be used but it can't be helped at this point.
crappy_things = string.letters + string.digits
def save_submission(song):
    extension = os.path.splitext(song.name)[1]

    salt = "".join(random.choice(crappy_things) for x in xrange(15))

    filename = "{:s}{:s}".format(salt, extension)

    filepath = os.path.join(settings.SUBMISSION_FILE_LOCATION, filename)

    with open(filepath, "wb+") as f:
        for chunk in song.chunks():
            f.write(chunk)


def upload(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            handle_submission(request, form)
    else:
        form = SubmissionForm()

    return render(request, 'submit/submit.html', {
                                'form': form,
                                })
