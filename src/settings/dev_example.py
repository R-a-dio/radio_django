from .common import *

# We don't want django-pipeline to compile stuff in development
# If you want to test this, you need to have the LESS compiler installed
PIPELINE_COMPILERS = enable_pipeline_debug()


DEBUG = True
TEMPLATE_DEBUG = DEBUG


# Location we put user submitted tracks, this is relative to MEDIA_ROOT
SUBMISSION_FILE_PATH = "music/"

# The database settings, see Django docs for info
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Haystack search settings, see documenation for help:
# http://django-haystack.readthedocs.org/en/latest/tutorial.html#modify-your-settings-py
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': '',
        'PATH': '',
    },
}

# The broker URL to use for django celery. See for details this:
# http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html
BROKER_URL = ''


# The part below is for setting up sentry, it will automatically setup a
# handler for several 3rd party apps to use the sentry handler instead.

# See your friendly sentry control panel for help.
# RAVEN_CONFIG = {
#    'dsn': '',
# }

# The parts underneath are for extra Sentry setup, don't touch it,
# it won't run unless RAVEN_CONFIG above is set.
try:
    dsn = RAVEN_CONFIG['dsn']
except NameError, KeyError:
    pass
else:
    from custom_settings import INSTALLED_APPS
    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    from raven.handlers.logging import SentryHandler
    import logging

    handler = SentryHandler(dsn)

    # Handler addition for thumbnail failures
    logging.getLogger('sorl.thumbnail').addHandler(handler)
