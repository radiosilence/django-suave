from django.contrib import admin

import reversion

from .models import Page, Section


class SiteEntityAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class DisplayableAdmin(SiteEntityAdmin):
    pass


class PageAdmin(DisplayableAdmin):
    pass


class SectionAdmin(DisplayableAdmin):
    pass


admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
