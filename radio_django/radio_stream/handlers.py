from haystack.query import SearchQuerySet
from radio_django.api import container
from radio_stream.models import Songs
from django.conf.urls import url
from django.http import Http404
from django.core.paginator import Paginator, InvalidPage
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

class SongResource(ModelResource):
    class Meta:
        queryset = Songs.objects.all().order_by('-id')
        resource_name = 'songs'
        allowed_methods = ['get']
        fields = ['metadata', 'length', 'id', 'hash']
        max_limit = 20

    def prepend_urls(self):
        return [
            url(r'^(?P<resource_name>%s)/search%s$' % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_song_search"),
        ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        sqs = SearchQuerySet().models(Songs).load_all().auto_query(request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("No such page exists.")
        except ValueError:
            raise Http404("Invalid page number.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        self.log_throttled_access(request)

        return self.create_response(request, {'objects': objects})


# Register ourself with the API urls
container.register(SongResource())
