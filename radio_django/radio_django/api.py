from tastypie.api import Api
from django.conf import settings

# If we are in development mode it's a lot easier
# if we have prettified JSON output on the APIs
if settings.DEBUG:
    import json as simplejson
    from django.core.serializers import json
    from tastypie.serializers import Serializer

    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return simplejson.dumps(data, cls=json.DjangoJSONEncoder,
                                sort_keys=True, ensure_ascii=False, indent=2)

    Serializer.to_json = to_json

container = Api(api_name='v1')

import radio_collection.search.handlers
radio_collection.search.handlers
import radio_stream.queue.handlers
radio_stream.queue.handlers
