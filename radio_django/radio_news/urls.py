from django.conf.urls import url, patterns


urlpatterns = patterns('radio_news.views',
    url(r"^$", 'index', name="news_index"),
    url(r"^(?P<page>\d+)/$", 'index', name="news_index_page"),
    url(r"^(?P<slug>\w+)/$", 'by_slug', name="news_by_slug"),
    url(r"^id/(?P<news_id>\d+)/$", 'by_id', name="news_by_id"),
)
