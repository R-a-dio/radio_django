Installation Requirements
=========================

Before we begin, it is highly recommended you install inside a `virtualenv`. If you don't want to have too much trouble installing `xapian` mentioned below, we suggest to use `virtualenv --system-site-packages` since the `xapian-bindings` will install into the system site packages by default.

You currently have to install `xapian` by yourself before installing this project. This includes all the requirements to use it from Python. The following needs to be installed.

`xapian-core`, `xapian-bindings` (at least Python ones), `xapian-haystack` from github and `django-haystack` from github. We are using the latest versions of the last two that don't have a pip package yet. To install them you can issue the following two commands:

`pip install -e git+https://github.com/toastdriven/django-haystack.git@master#egg=django-haystack`
`pip install -e git+https://github.com/notanumber/xapian-haystack.git@master#egg=xapian-haystack`


Installation
============

You have to create your own `local_settings.py` in `/radio_django/radio_django/radio_django/local_settings.py` (Don't you love that long path.), it should contains the following template with your own relevant info filled in.


    # Local Settings - Settings that are specific to a development environment (
    # e.g. DATABASES, INTERNAL_IPS, INSTALLED_APPS, etc.)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

    HAYSTACK_CONNECTIONS = {
    	'default': {
    		'ENGINE': 'haystack.backends.xapian_backend.XapianEngine',
    		'PATH': '',
    	},
    }

    # INTERNAL_IPS = ('127.0.0.1',)

    from custom_settings import INSTALLED_APPS
    INSTALLED_APPS += (
        #'debug_toolbar',
    )
