from haystack.query import SearchQuerySet
from radio_django.api import container
from radio_collection.models import Tracks, Albums, Artists
from radio_collection.search import RESULTS_PER_PAGE
from django.conf.urls import url
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from tastypie.fields import ForeignKey

class ArtistResource(ModelResource):
    class Meta:
        queryset = Artists.objects.all().order_by('-id')
        resource_name = 'artists'
        allowed_methods = ['get']
        fields = ['name', 'id']
        max_limit = 20


class AlbumResource(ModelResource):
    class Meta:
        queryset = Albums.objects.all().order_by('-id')
        resource_name = 'albums'
        allowed_methods = ['get']
        fields = ['name', 'id']
        max_limit = 20


class TrackResource(ModelResource):
    artist = ForeignKey(ArtistResource, 'artist',
                        full=True, null=True, blank=True, full_list=True)
    album = ForeignKey(AlbumResource, 'album',
                       full=True, null=True, blank=True, full_list=True)
    class Meta:
        queryset = Tracks.objects.all().order_by('-id')
        resource_name = 'tracks'
        allowed_methods = ['get']
        fields = ['title', 'length', 'id', 'album', 'artist']
        max_limit = 20

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/search%s$' % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_track_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        sqs = SearchQuerySet().models(Tracks).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, RESULTS_PER_PAGE)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("No such page exists.")
        except ValueError:
            raise Http404("Invalid page number.")

        objects = []

        for result in page.object_list:
            if result is None: continue
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        self.log_throttled_access(request)

        return self.create_response(request, {'objects': objects})


# Register ourself with the API urls
container.register(TrackResource())
container.register(ArtistResource())
container.register(AlbumResource())
