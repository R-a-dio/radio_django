from datetime import datetime
import functools

from django.template import Library


register = Library()


def attribute_receiver(func):
    @functools.wraps(func)
    def wrapper(value, attribute=None, *args, **kwargs):
        if attribute is not None:
            value = getattr(value, attribute, value)
        return func(value, *args, **kwargs)
    return wrapper


@register.filter
@attribute_receiver
def search_time_format(value):
    try:
        return value.strftime('%a %d %b, %H:%M')
    except AttributeError:
        return u'Never'


@register.filter
@attribute_receiver
def time_format(value):
    return value.strftime('%H:%M:%S')


@register.filter
@attribute_receiver
def limit_time_format(value):
    delta = datetime.now() - value
    if delta >= 1:
        return "{days:d} day{plural:s} ago".format(
            days=delta.days,
            plural='' if delta.days == 1 else 's',
        )
    return time_format(value)
