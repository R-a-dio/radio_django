from django.conf import settings
import os.path
import hashlib


def generate_music_filename(filename):
    """
    Generates a filename that is 15 random chars + `extension` given.

    This is used to avoid having a 'too public' approachable database of our music files.
    """
    extension = os.path.splitext(filename)[1]

    new_filename = hashlib.md5(filename + salt).hexdigest()

    return "{:s}{:s}".format(new_filename, extension)


def generate_music_filename_field(instance, original_filename):
    """
    Gives out a proper filename for saving music files with a FileField.

    You can give this function as argument to a FileFields `upload_to`.
    """

    instance.original_filename = original_filename

    new_filename = generate_music_filename(original_filename)

    return os.path.join(settings.SUBMISSION_FILE_PATH, new_filename[:4], new_filename)
