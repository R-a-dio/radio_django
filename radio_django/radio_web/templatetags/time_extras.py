from django.template import Library
from datetime import datetime

register = Library()

@register.filter
def search_time_format(value):
    try:
        return value.strftime('%a %d %b, %H:%M')
    except AttributeError:
        return u'Never'

@register.filter
def time_format(value):
    return value.strftime('%H:%M:%S')

@register.filter
def limit_time_format(value):
    delta = datetime.now() - value
    if delta >= 1:
        return "{days:d} day{plural:s} ago".format(days=delta.days, plural='' if delta.days == 1 else 's')
    return time_format(value)
