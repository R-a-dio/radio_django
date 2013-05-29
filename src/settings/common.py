from path import path

# Make sure to create your own SECRET_KEY
# Make this unique, and don't share it with anybody.
SECRET_KEY = '+4djssa@%hebp*h%cpy4f)wx_8eidfl7kuxc-gwql_0z)qo5hi'

GRAPPELLI_ADMIN_TITLE = "R/a/dio admin panel"


PROJECT_ROOT = path(__file__).abspath().dirname().dirname()

STATIC_URL = path('/static/')
MEDIA_ROOT = PROJECT_ROOT / 'static' / 'media'
MEDIA_URL = STATIC_URL / 'media/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'sorl.thumbnail',
    'gunicorn',
    'pipeline',
    'sitetree',
    'south',
    'haystack',
    'djcelery',
    'celery_haystack',
    'tastypie',
    'reversion',
    'endless_pagination',
    'radio_news',
    'radio_stream',
    'radio_collection',
    'radio_users',
    'radio_web',
    'radio_django',
)


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT / 'static',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Setup django-pipeline
PIPELINE_CSS = {
    "radio_css": {
        'source_filenames': (
            "less/default/base.less",
            "css/default/*.css",
        ),
        "output_filename": 'css/radio.css',
    },
}

PIPELINE_JS = {
    "radio_js": {
        'source_filenames': (
            "js/bootstrap.js",
            "js/custom/*.js",
        ),
        "output_filename": 'js/radio.js',
    },
}

def enable_pipeline_debug():
    PIPELINE_JS['radio_js']['source_filenames'] += ("js/dev/less.min.js",)
    return tuple()

PIPELINE_COMPILERS = (
    'pipeline.compilers.less.LessCompiler',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None


# We don't want any of the less-safe formats to be used.
TASTYPIE_DEFAULT_FORMATS = ['json', 'xml', 'jsonp']

import mutagen.flac
import mutagen.mp3
import mutagen.oggvorbis

SUBMISSION_MAX_SIZE_MAPPING = {
    mutagen.flac.FLAC: 7.34e+7,
    mutagen.mp3.MP3: 15728640,
    mutagen.mp3.EasyMP3: 15728640,
    mutagen.oggvorbis.OggVorbis: 15728640,
}

# The amount of results on a common page
# The amount of search results can't be edited right now
PER_PAGE = 20

import datetime
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
