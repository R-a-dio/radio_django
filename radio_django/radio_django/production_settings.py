# Production Settings - Settings that are specific to a production environment (
# e.g. DEBUG, TEMPLATE_DEBUG, DATABASES, etc.)
import os


# We rarely ever want DEBUG enabled in production, so don't
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# The path to where we should put static files, it is recommended to have your
# webserver serve static files. So this is often inside your webroot somewhere.
STATIC_ROOT = '/path/to/my/webroot/static'

# The URL relative to the webroot for the static files.
# Note: Make sure you have the trailing forward slash
STATIC_URL = 'static/'

# Your media root, the default are quite sane so don't touch it unless needed
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'media/')
# Same as above but then as URL, if you change one of these you have to change
# the other as well.
MEDIA_URL = STATIC_URL + 'media/'

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

# Haystack search settings, see http://django-haystack.readthedocs.org/en/latest/tutorial.html#modify-your-settings-py for help.
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': '',
        'PATH': '',
    },
}

# The broker URL to use for django celery.
# See: http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html
BROKER_URL = ''


# The part below is for setting up sentry, it will automatically setup a handler for several 3rd party apps to
# use the sentry handler instead.

# See your friendly sentry control panel for help.
# RAVEN_CONFIG = {
#    'dsn': '',
# }

# The parts underneath are for extra Sentry setup, don't touch it, it won't run unless RAVEN_CONFIG is set.
try:
    dsn = RAVEN_CONFIG['dsn']
except:
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

