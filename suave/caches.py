import babylon
import hashlib

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from suave.utils import RequestFactory
from .models import Page, NavItem, PageContent

class PageCache(babylon.Cache):
    model = Page
    def generate(self, url, *args):
        page = get_object_or_404(Page, status='live', url=url)
        return page

babylon.register(PageCache)

class PageContentCache(babylon.Cache):
    model = PageContent
    key_attr = 'identifier'

    def generate(self, identifier=None, active=None, instance=None, *args):
        if instance:
            return instance
        elif identifier:
            try:
                return PageContent.objects.get(
                    Q(identifier=identifier),
                    Q(page=active) | Q(page=None)
                )
            except PageContent.DoesNotExist:
                return False
        else:
            return False

babylon.register(PageContentCache)
