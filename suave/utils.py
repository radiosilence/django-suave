import sys
from functools import wraps

from django.http import Http404
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django.db.models.signals import pre_save, post_save
from django.core.urlresolvers import reverse_lazy, reverse
from django.dispatch import receiver

from django.test import Client
from django.core.handlers.wsgi import WSGIRequest


from .models import pre_route, post_route, Image


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


class RequestFactory(Client):
    """
    Class that lets you create mock Request objects for use in testing.
    
    Usage:
    
    rf = RequestFactory()
    get_request = rf.get('/hello/')
    post_request = rf.post('/submit/', {'foo': 'bar'})
    
    This class re-uses the django.test.client.Client interface, docs here:
    http://www.djangoproject.com/documentation/testing/#the-test-client
    
    Once you have a request object you can pass it to any view function, 
    just as if that view had been hooked up using a URLconf.
    
    """
    def request(self, **request):
        """
        Similar to parent class, but returns the request object as soon as it
        has created it.
        """
        environ = {
            'HTTP_COOKIE': self.cookies,
            'PATH_INFO': '/',
            'QUERY_STRING': '',
            'REQUEST_METHOD': 'GET',
            'SCRIPT_NAME': '',
            'SERVER_NAME': Site.objects.get_current().domain,
            'SERVER_PORT': 80,
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.input': None
        }
        environ.update(self.defaults)
        environ.update(request)
        return WSGIRequest(environ)