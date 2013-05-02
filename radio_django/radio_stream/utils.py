from django.core.cache import cache
from radio_stream.models import Songs


def retrieve_current_song():
    """
    Retrieves the current playing Song from cache and returns it.

    return: Songs object or None
    """
    current_id = cache.get("radio_current_song")
    if current_id is None:
        return None
    return Songs.objects.get(pk=current_id)
