from django.utils.timezone import utc
from django.core.cache import cache
from django.conf.urls import url
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication
from tastypie.fields import ForeignKey
from radio_django.api import container
from radio_stream.models import Queue, Songs
from radio_stream.handlers import SongResource
from radio_stream.queue.serializer import QueueSerializer
from radio_users.models import Djs
from copy import copy
import collections
import datetime

# Datetimes are formatted according to http://www.ecma-international.org/ecma-262/5.1/#sec-15.9.1.15

class WriteDjangoAuthorization(DjangoAuthorization):
    """
    A simple subclass that makes read-only access require no authorization.
    """
    def is_authorized(self, request, object=None):
        if request.method == 'GET':
            return True
        else:
            return super(WriteDjangoAuthorization, self).is_authorized(request, object)

class WriteBasicAuthentication(BasicAuthentication):
    """
    A simple subclass that makes read-only access require no authentication.
    """
    def is_authenticated(self, request, **kwargs):
        if request.method == 'GET':
            return True
        else:
            return super(WriteBasicAuthentication, self).is_authenticated(request)

class QueueResource(ModelResource):
    song = ForeignKey(SongResource, 'song',
                      full=True, null=True, blank=True)

    class Meta:
        queryset = Queue.objects.all().order_by('time')
        resource_name = "queue"
        allowed_methods = ['get', 'post', 'delete']
        authorization = WriteDjangoAuthorization()
        authentication = WriteBasicAuthentication()
        include_resource_uri = False
        serializer = QueueSerializer()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<user>\d+)/$" % self._meta.resource_name,
                self.wrap_view('get_queue_list'), name="api_queue_list"),
        ]
    
    def create_error_response(self, request, err_msg, err_number, status=500, **kwargs):
        """
        Returns a generic bundle that is populated with information given.

        The standard response looks similar to this:
            `{"error": {"msg": "My error message", "id": -1}}`

        And will by default send a HTTP status code of 500.
        """
        response = self.create_response(request, {"error": dict(msg=err_msg, id=err_number, **kwargs)})
        response.status_code = status
        return response

    def get_list(self, request, **kwargs):
        user = cache.get('radio_current_dj')
        return self.get_queue_list(request, user=user, **kwargs)

    def get_queue_list(self, request, user, **kwargs):
        """
        Returns the queue of the given DJ id, if no DJ with the id is found an error will be raised.

        The errors that can be raised are the following:
            (-1, Invalid DJ found): Indicates that there is no current DJ set in the system.
            (-2, DJ found is not an integer): Indicates that the user input, or the system returned
                                              something that isn't an integer.
            (-3, No DJ with that ID found): Indicates that no DJ exists with the ID given.
        """
        base_bundle = self.build_bundle(request=request)
        objects = self.obj_get_list(bundle=base_bundle)

        if user is None:
            return self.create_error_response(request, u"Invalid DJ found", -1)

        try:
            dj_id = int(user)
        except TypeError:
            return self.create_error_response(request, u"DJ found is not an integer.", -2)

        try:
            Djs.objects.get(pk=dj_id)
        except Djs.DoesNotExist:
            return self.create_error_response(request, u"No DJ with that ID found.", -3)

        objects = objects.filter(user__id=dj_id)
        
        # Add pagination after filtering!
        paginator = self._meta.paginator_class(request.GET, objects,
                                               resource_uri=self.get_resource_uri(),
                                               limit=self._meta.limit,
                                               max_limit=self._meta.max_limit,
                                               collection_name=self._meta.collection_name)
        to_be_serialized = paginator.page()


        bundles = []

        for obj in to_be_serialized[self._meta.collection_name]:
            bundle = self.build_bundle(obj=obj, request=request)
            bundles.append(self.full_dehydrate(bundle, for_list=True))

        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def post_list(self, request, **kwargs):
        """
        Called whenever someone does a post to `/api/v/queue/`
        
        """
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('content_type', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        
        result = self.validate_queue(request, deserialized)
        if result is None:
            return super(QueueResource, self).post_list(request, **kwargs)
        return result

    def validate_queue(self, request, data):
        """
        Responsible for validating the input from the user, the input is an already
        deserialized python object. Validation should either return None or a response
        to return to the user.
        """
        # First lets make sure the user has a DJ account
        try:
            dj = request.user.dj_account
        except Djs.DoesNotExist:
            return self.create_error_response(request, u"You don't have a DJ account.", -1)

        # Validate the 'current' entry if it exists
        if 'current' in data:
            # Both entries should be integers
            try:
                int(data['current']['position'])
                int(data['current']['length'])
            except TypeError:
                return self.create_error_response(request,
                            u"Value of `position` or `length` is not an integer.", -2)

        if 'queue' not in data:
            return self.create_error_response(request,
                            u"Empty queue received, to delete a queue use DELETE.", -3)

        if not isinstance(data['queue'], list):
            return self.create_error_response(request,
                            u"Queue should've been a list type.", -7)

        for song in data['queue']:
            # Do we have any of the keys at all~
            if not "metadata" in song or not "length" in song:
                return self.create_error_response(request,
                            u"Missing one of the required fields `metadata` and `length`.", -6)

            # check if length is an integer or not
            try:
                int(song['length'])
            except TypeError:
                return self.create_error_response(request,
                            u"`length` value is not an integer.", -4)
            # Make sure the metadata is a string type.
            if not isinstance(song['metadata'], (unicode, str, bytes)):
                return self.create_error_response(request,
                            u"`metadata` value is not a string.", -5)


    def obj_create(self, bundle, **kwargs):
        data = bundle.data
        
        dj = bundle.request.user.dj_account

        # Check if we have an offset for the queue start
        current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
        if 'current' in data:
            position = int(data['current']['position'])
            length = int(data['current']['length'])
            
            current_time += datetime.timedelta(seconds=length - position)


        queue = data['queue']

        song_hashes = []
        for i, song in enumerate(queue[:]):
            
            metadata = song['metadata']

            # Convert all our dicts to namedtuples
            queue[i] = SongTuple(length=int(song['length']),
                                 metadata=metadata)

            # Create a hash and append to our list
            song_hashes.append(Songs.create_hash(metadata))

        song_objects = Songs.objects.filter(hash__in=song_hashes)

        song_obj_hashes = {obj.hash: obj for obj in song_objects}

        songs = []
        for song, song_hash in zip(queue, song_hashes):
            obj = song_obj_hashes.get(song_hash, None)
            if obj is None:
                obj = Songs.objects.create(metadata=song.metadata,
                                           length=song.length,
                                           hash=song_hash)
                song_obj_hashes[obj.hash] = obj

            songs.append(obj)

        Queue.objects.filter(user=dj.user).delete()

        queue_objects = []
        for obj in songs:
            queue_objects.append(
                    Queue(song=obj, user=dj, time=copy(current_time))
            )
            current_time += datetime.timedelta(seconds=obj.length)

        Queue.objects.bulk_create(queue_objects)

SongTuple = collections.namedtuple('SongTuple', ('length', 'metadata'))

container.register(QueueResource())
