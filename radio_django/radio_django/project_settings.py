# Project Settings - Settings that don't exist in settings.py that you want to
# add (e.g. USE_THOUSAND_SEPARATOR, GRAPPELLI_ADMIN_TITLE, CELERYBEAT_SCHEDULER,
# CELERYD_PREFETCH_MULTIPLIER, etc.)

#USE_THOUSAND_SEPARATOR = True

TASTYPIE_DEFAULT_FORMATS = ['json', 'xml', 'jsonp']
#GRAPPELLI_ADMIN_TITLE = ''

import mutagen.flac, mutagen.mp3, mutagen.oggvorbis
import datetime
SUBMISSION_MAX_SIZE_MAPPING = {
    mutagen.flac.FLAC: 7.34e+7,
    mutagen.mp3.MP3: 15728640,
    mutagen.mp3.EasyMP3: 15728640,
    mutagen.oggvorbis.OggVorbis: 15728640,
}
# The amount of results on a common page
# The amount of search results can't be edited right now
RESULTS_PER_PAGE = 20

# This is the time between track submissions,
# if you want to change this add your own definition in local_settings.py
SUBMISSION_DELAY = datetime.timedelta(hours=2)


# Celery settings, shouldn't be touched unless you know what you are doing.
import djcelery
djcelery.setup_loader()
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERYD_PREFETCH_MULTIPLIER = 1

# Setup a celery processor for haystack index updates.
HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.CelerySignalProcessor'


import os
import sys

if 'PRODUCTION' in os.environ and os.environ['PRODUCTION'].lower() in [True, 'y', 'yes', '1',]:
    from production_settings import *
else:
    from local_settings import *
