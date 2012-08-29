import sys
from functools import wraps

from django.http import Http404
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.safestring import mark_safe
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse_lazy, reverse
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


def add_link_field(target_model=None, field='', link_text=unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            link_obj = getattr(instance, field, None) or instance
            app_name = link_obj._meta.app_label
            reverse_path = "admin:{}_{}_change".format(app_name, reverse_name)
            url = reverse(reverse_path, args=(link_obj.id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name + ' link'
        cls.link = link
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + ['link']
        return cls
    return add_link
