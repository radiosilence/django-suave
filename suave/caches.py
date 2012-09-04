import babylon
import hashlib

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from suave.utils import RequestFactory
from .models import Page, NavItem

class PageCache(babylon.Cache):
    model = Page
    def generate(self, url):
        page = get_object_or_404(Page, status='live', url=url)
        return page

babylon.register(PageCache)
