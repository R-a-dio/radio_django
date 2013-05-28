Django App explanation
======================

The current layout of this directory is split by functionality. We list each app here with what functionality it provides in the general sense.


radio collection
----------------

This is the app responsible for things related to our AFK streamer music database. We've decided to split up our general data and AFK data in this project. Anything related to the AFK streamer is highly likely to go in here. If you are unsure of where to put something new, ask someone on the dev team.


radio django
------------

This app contains settings of the project and the root `urls.py`. Nothing else is really here.

For information about the different settings file see the original repository. We use a clone of [django-settings](https://github.com/django-settings/django-settings).


radio news
----------

This app contains all the logic related to our news system. Which is relatively small and feature-less.


radio stream
------------

Logic related to any of our stream data. Such as play data, queues, statistics and other things related to the stream that are NOT related to the AFK streamer.


radio users
-----------

Any logic related to our user data, this includes things like our staff page, the favourites system and other things related to user data.


radio web
---------

Things that are website specific and less r/a/dio related. Example is the front page.
