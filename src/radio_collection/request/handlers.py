from radio_collection.models import Requests
from piston.handler import BaseHandler
from piston.utils import rc


class RequestHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Requests
