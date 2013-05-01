from django.template import Library

register = Library()

@register.filter
def search_time_format(value):
    try:
        return value.strftime('%a %d %b, %H:%M')
    except AttributeError:
        return u'Never'
