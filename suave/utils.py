from django.core.cache import cache
from .models import Page


def get_page_from_url(url):
    key = 'suave:page_at_url:%s' % url
    page = cache.get(key)
    if page == None:
        if url[-1] != '/':
            url = url + '/'

        if url[0] != '/':
            url = '/' + url
        try:
            page = Page.objects.live().get(url=url)
        except Page.DoesNotExist:
            page = False

    cache.set(key, page, 60)
    return page
