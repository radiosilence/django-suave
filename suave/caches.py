import babylon
import hashlib

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from suave.utils import RequestFactory
from .models import Page, NavItem, ContentBlock

class PageCache(babylon.Cache):
    model = Page
    key_attr = 'url'

babylon.register(PageCache)

class RenderedPageCache(babylon.Cache):
    model = Page
    key_attr = 'url'
    extra_delete_args = (False, True)
    dependencies = (
        PageCache,
    )
    def generate(self, url=False, pjax=False, request=False, *args, **kwargs):
        def fix_url(url):
            if url[-1] != '/':
                url = url + '/'

            if url[0] != '/':
                url = '/' + url
            return url

        if not request:
            return False
        try:
            url = fix_url(url)
            page = babylon.get('PageCache', url)
            if not page:
                raise Page.DoesNotExist
            template = page.template_override
            if not template:
                template = 'page.html'

            parent = 'base.html'
            if pjax:
                parent = 'pjax.html'

            return TemplateResponse(request, template, {
                'active': page,
                'page': page,
                'parent': parent
            }).render().content

        except Page.DoesNotExist:
            return False


        return page

babylon.register(RenderedPageCache)


class ContentBlockCache(babylon.Cache):
    model = ContentBlock
    key_attr = 'identifier'

babylon.register(ContentBlockCache)
