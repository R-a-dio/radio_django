from django.core.cache import cache
from radio_users.models import Djs


def retrieve_current_dj():
    """
    Retrieves the current DJ from cache and returns it.

    return: Djs object or None
    """
    dj_id = cache.get("radio_current_dj")
    if dj_id is None:
        return Djs.objects.get(name="None")
    return Djs.objects.get(pk=dj_id)
