from django.core.cache import cache
from .models import Page


def get_page_from_url(url):
    key = 'suave:page_at_url:%s' % url
    page = cache.get(key)
    if page == None:
        if url[-1] != '/':
            url = url + '/'
        if url == '/':
            page = Page.objects.all()[0].get_root()
        else:
            page = False
            slug = url.split('/')[-2]
            for attempt in Page.objects.filter(slug=slug).live().all():
                if attempt.url.strip('/') == url.strip('/'):
                    page = attempt
                    break
    cache.set(key, page, 60)
    return page
