# Project Settings - Settings that don't exist in settings.py that you want to
# add (e.g. USE_THOUSAND_SEPARATOR, GRAPPELLI_ADMIN_TITLE, CELERYBEAT_SCHEDULER,
# CELERYD_PREFETCH_MULTIPLIER, etc.)

#USE_THOUSAND_SEPARATOR = True

#GRAPPELLI_ADMIN_TITLE = ''

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
