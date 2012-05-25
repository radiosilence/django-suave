from django.http import Http404
from django.core.cache import cache

from .models import Page


def get_page_from_url(url):
    if url[-1] != '/':
        url = url + '/'

    if url[0] != '/':
        url = '/' + url
    try:
        return Page.objects.select_related().live().get(url=url)
    except Page.DoesNotExist:
        raise Http404


