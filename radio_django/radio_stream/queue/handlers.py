from django.core.cache import cache
from piston.handler import BaseHandler
from piston.utils import rc, require_mime
from radio_stream.models import Queue, Songs
from radio_users.models import Djs


class QueueHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    model = Queue

    def read(self, request, dj=None):
        if dj is None:
            # Get the DJ from our memcache instead
            dj = cache.get('radio_current_dj')
        
        if dj is None:
            # We couldn't find a DJ to use.
            return rc.NOT_FOUND

        try:
            dj = int(dj)
        except TypeError:
            return rc.BAD_REQUEST
        
        try:
            dj_obj = Djs.objects.get(pk=dj)
        except Djs.DoesNotExist:
            return rc.BAD_REQUEST

        return Queue.objects.all().filter(user=dj_obj)
        
    @require_mime('json')
    def create(self, request):
        user = request.user
        if request.content_type == 'application/json':
            data = request.data
            # The json is of format {'current': {'length': n, 'position': n}, 'queue': [<tracks>, ...]}
            # <tracks> = {'metadata': 'a string of metadata', 'length': n}
            # both length and position should be integers in seconds
            current_time = datetime.datetime.now()
            if u'current' in data:
                # Parse our offset for the data.
                offset = int(data['length']) - int(data['position'])
                current_time += datetime.timedelta(seconds=offset)

            if u'queue' not in data:
                # No queue send at all, bad request
                return rc.BAD_REQUEST
            
            queue = data['queue']

            # validation
            if not isinstance(queue, list):
                # The queue received isn't a list? wat
                return rc.BAD_REQUEST
            
            song_hashes = []
            for song in queue:
                # validation
                if not u'metadata' in song or not u'length' in song:
                    # Missing required field on song dict
                    return rc.BAD_REQUEST
                # make sure we got an actual integer and convert it so we don't have to worry later
                song['length'] = int(song['length'])

                song_hash = Songs.create_hash(song['metadata'])
                
                song_hashes.append(song_hash)

            # From this point forward we've validated all the data received already, we can stop wondering
            # about us having correct data or not.

            # We get all songs that already exist in the database
            song_objs = Songs.objects.filter(hash__in=song_hashes)
            # Create a dict mapping for faster lookup times
            song_obj_hashes = {obj.hash: obj for obj in song_objs}

            # The list of final song objects, all ready to relate to
            songs = []
            for song, song_hash in zip(queue, song_hashes):
                obj = song_obj_hashes.get(song_hash, None)
                if obj is None:
                    # We have no song entry yet, create one. This is done one-by-one.
                    obj = Songs.objects.create(meta=song['metadata'],
                                               length=song['length'],
                                               hash=song_hash)
                songs.append(obj)

            # Delete old objects
            Queue.objects.filter(user=user).delete()
            
            queue_objs = []
            for obj in songs:
                # Make sure we increase our estimated queue time
                current_time += datetime.timedelta(seconds=obj.length)
                # and at a Queue object to our list of objects
                queue_objs.append(Queue(song=obj, user=user, time=copy(current_time)))

            # Create the list of objects, and done we are~
            Queue.objects.bulk_create(queue_objs)

            return rc.CREATED
        else:
            # We have no idea what that content type is
            return rc.BAD_REQUEST

    @require_mime('json')
    def update(self, request):
        pass
