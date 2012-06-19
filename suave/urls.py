from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('suave.views',
    url(r'^(?P<url>[a-z0-9\-\/]+)/$', 'page', name='page'),
    url(r'^$', 'page', name='page'),
)
