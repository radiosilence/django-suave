from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('suave.views',
    url(r'^(?P<section_slug>[a-z\-]*)/(?P<page_slug>[a-z\-]*)/$',
        'page', name='page',),
    url(r'^(?P<section_slug>[a-z\-]*)/$',
        'page', name='page',),
    url(r'^$', 'page', name='page'),
)
