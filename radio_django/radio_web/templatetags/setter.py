from django import template


register = template.Library()


@register.assignment_tag
def setter(value):
    return value
