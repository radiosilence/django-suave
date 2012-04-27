from django.core.cache import cache
from .models import Page


def get_page_from_url(url):
    key = 'suave:page_at_url:%s' % url
    page = cache.get(key)
    if page == None:
        page = False
        for attempt in Page.objects.live().all():
            if attempt.url.strip('/') == url.strip('/'):
                page = attempt
                break
    cache.set(key, page, 60)
    return page
