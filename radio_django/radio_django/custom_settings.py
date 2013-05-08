# Custom Settings - Settings that exist in settings.py that you want to
# override or append to (e.g. ADMINS, TIME_ZONE, MEDIA_ROOT, MEDIA_URL,
# STATIC_ROOT, MIDDLEWARE_CLASSES, TEMPLATE_DIRS, INSTALLED_APPS, etc.)

#ADMINS = (('Django Settings', 'django-settings@example.com'),)

TIME_ZONE = 'Europe/Amsterdam'

#MEDIA_ROOT = 'media'

#MEDIA_URL = '/media/'

#STATIC_ROOT = 'static'

import os.path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

from settings import STATICFILES_DIRS
STATICFILES_DIRS += (
    os.path.join(PROJECT_ROOT, "..", "static"),
)

from settings import MIDDLEWARE_CLASSES
MIDDLEWARE_CLASSES += (
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
)

from settings import TEMPLATE_DIRS
TEMPLATE_DIRS += (
    #'',
)

from settings import TEMPLATE_LOADERS
TEMPLATE_LOADERS += (
    'django.template.loaders.app_directories.Loader',
)

from settings import INSTALLED_APPS
INSTALLED_APPS += (
    'grappelli',
    #'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'sitetree',
    'south',
    'haystack',
    'djcelery',
    'celery_haystack',
    'tastypie',
    'reversion',
    'radio_news',
    'radio_stream',
    'radio_collection',
    'radio_users',
    'radio_web',
    'radio_django',
)

from project_settings import *
