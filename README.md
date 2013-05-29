[![Build Status](https://travis-ci.org/Wessie/radio_django.png)](https://travis-ci.org/Wessie/radio\_django)
[![codeq](https://codeq.io/github/Wessie/radio_django/badges/master.png)](https://codeq.io/github/Wessie/radio\_django/branches/master)


Installation
============

The following packages are required to install the project:

`apt-get install python-dev libpq-dev libjpeg62-dev`

then you can do the following to install all the required python dependencies:

`pip install -r requirements.txt`

Extra functionality or preferences might require extra packages to be installed.


Search functionality
--------------------

If you want to use search functionality you have to install a search engine for use by haystack. For more information about this you can look at the [documentation](https://django-haystack.readthedocs.org/en/latest/installing_search_engines.html) of haystack itself.

Database
--------

The database used for development isn't very important and you can get by with using `sqlite3`. For database setup we point you towards the Django documentation on [database setup](https://docs.djangoproject.com/en/1.5/topics/install/#database-installation)

Celery
------

Celery requires a message broker to be installed. We suggest using RabbitMQ, instructions can be found at the [celery project documentation](http://docs.celeryproject.org/en/latest/getting-started/brokers/rabbitmq.html) Don't forget to set the `BROKER_URL` in `local_settings.py`.

LESS
----

NOTE: For development this is not a requirement.

We use LESS for our stylesheets, you need the LESS compiler for this to work correctly. Instructions can be found at the [less documentation](http://lesscss.org/#usage)(Scroll down to server side usage).


Settings
========

A bare settings file can be found in `src/settings/local_example.py`. Make a copy of this file to something like `src/settings/development.py` or `src/settings/production.py`. Then set the `DJANGO_SETTINGS_MODULE` environment variable to the file you just created, if you named it `development.py` you do `export DJANGO_SETTINGS_MODULE=settings.development`. Replace `development` with what you named it.

Then open your new file and edit the settings to your liking. Before continueing.

Database initializing
---------------------

To finish up you need to run the following management commands for Django

`manage.py syncdb`
`manage.py migrate`

Running the server
==================

For development you can simple do a `manage.py runserver`. For all other uses you should really take a look at the django documentation for deployment.

