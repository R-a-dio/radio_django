# Project Settings - Settings that don't exist in settings.py that you want to
# add (e.g. USE_THOUSAND_SEPARATOR, GRAPPELLI_ADMIN_TITLE, CELERYBEAT_SCHEDULER,
# CELERYD_PREFETCH_MULTIPLIER, etc.)

#USE_THOUSAND_SEPARATOR = True

#GRAPPELLI_ADMIN_TITLE = ''

import mutagen.flac, mutagen.mp3, mutagen.oggvorbis
import datetime
SUBMISSION_MAX_SIZE_MAPPING = {
    mutagen.flac.FLAC: 7.34e+7,
    mutagen.mp3.MP3: 15728640,
    mutagen.oggvorbis.OggVorbis: 15728640,
}

SUBMISSION_DELAY = datetime.timedelta(hours=2)
SUBMISSION_FILE_LOCATION = "/tmp"

import djcelery
djcelery.setup_loader()
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYD_PREFETCH_MULTIPLIER = 1

# Setup a queue processor.
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'


import os
import sys

if 'PRODUCTION' in os.environ and os.environ['PRODUCTION'].lower() in [True, 'y', 'yes', '1',]:
    from production_settings import *
else:
    from local_settings import *
