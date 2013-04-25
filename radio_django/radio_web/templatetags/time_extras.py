from django.template import Library

register = Library()

@register.filter
def search_time_format(value):
    if value is None:
        return u'Never'
    return value.strftime('%a %d %b, %H:%M')
