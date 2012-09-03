import babylon
import hashlib

from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Page

class PageCache(babylon.Cache):
    model = Page
    def _fix_url(self, url):
        if url[-1] != '/':
            url = url + '/'

        if url[0] != '/':
            url = '/' + url
        return url

    def key(self, url, request):
        url = self._fix_url(url)

        key = '{}:{}:pjax={}'.format(
            self.__class__.__name__, url,
            request.META.get('HTTP_X_PJAX', 'False')
        )

        return hashlib.sha1(key).hexdigest()

    def invalidate(self, sender, instance, *args, **kwargs):
       self.set(instance.url, self.generate(instance.url))
       for parent in self._parents:
            parent.invalidate(instance)

    def generate(self, url, request):
        url = self._fix_url(url)
        page = get_object_or_404(Page, status='live', url=url)
        template = page.template_override
        if not template:
            template = 'page.html'

        parent = 'base.html'
        if request.GET.get('HTTP_X_PJAX', False):
            print "PJAX REQUST"
            parent = 'pjax.html'

        return TemplateResponse(request, template, dict(
            active=page,
            page=page,
            parent=parent
        )).content

babylon.register(PageCache)