from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import Page


class SiteEntityAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class DisplayableAdmin(SiteEntityAdmin):
    pass


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    pass


admin.site.register(Page, PageAdmin)
