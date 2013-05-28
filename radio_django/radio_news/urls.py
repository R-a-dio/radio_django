from django.conf.urls import url, patterns


urlpatterns = patterns(
    'radio_news.views',
    url(r"^$", 'index', name="radio-news"),
    url(r"^(?P<page>\d+)/$", 'index', name="radio-news-pagination"),
    url(r"^(?P<slug>\w+)/$", 'by_slug', name="radio-news-slug"),
    url(r"^id/(?P<news_id>\d+)/$", 'by_id', name="radio-news-id"),
)
