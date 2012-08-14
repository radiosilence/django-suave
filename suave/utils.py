import sys
from functools import wraps

from django.http import Http404
from django.conf import settings
from django.utils.importlib import import_module
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Page, pre_route, post_route, Image


def pre_url(route_url):
    def outer(f):
        @wraps(f)
        def wrapper(sender, url, **kwargs):
            if route_url == url:
                return f(request=sender, url=url)
            else:
                return False
        pre_route.connect(wrapper)
        return wrapper
    return outer


def get_page_from_url(url):
    if url[-1] != '/':
        url = url + '/'

    if url[0] != '/':
        url = '/' + url
    try:
        return Page.objects.select_related().live().get(url=url)
    except Page.DoesNotExist:
        raise Http404


def get_default_image():
    try:
        return Image(image=settings.DEFAULT_IMAGE)
    except AttributeError:
        return None