from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('suave.views',
    url(r'^(?P<url>[-\w\/]+)/$', 'page', name='page'),
    url(r'^$', 'page', name='page'),
)
