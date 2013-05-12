from django import template

register = template.Library()

@register.filter
def page_url(page, request):
    get = request.GET.copy()
    get['page'] = page
    return "?{:s}".format(get.urlencode())
