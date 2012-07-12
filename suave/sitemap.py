from django.contrib.sitemaps import Sitemap
from .models import Page


class PageSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Page.objects.live()

    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.url
