from django.conf.urls import patterns, include, url
from posts.models import Post

urlpatterns = patterns('posts.views',
    # url(r'^balonline/', include('balonline.foo.urls')),
    url('^$', 'index'),
    url(r'(?P<post_id>\d+)/$', 'detail'),
    url(r'archive$', 'archive'),
)
