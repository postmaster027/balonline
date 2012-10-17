from django.conf.urls import patterns, include, url
from ymapscatalog.models import Firm

urlpatterns = patterns('ymapscatalog.views',
    # url(r'^balonline/', include('balonline.foo.urls')),
    url('^$', 'index'),
    url(r'(?P<firm_id>\d+)/$', 'detail'),
    url(r'^tag/(?P<tag>[^/]+)/$', 'tagged'),
    url(r'traffic/$', 'traffic'),
)


