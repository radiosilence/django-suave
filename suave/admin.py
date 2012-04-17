from django.contrib import admin

from .models import Page, Section


class SiteEntityAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class DisplayableAdmin(SiteEntityAdmin):
    pass


class PageAdmin(DisplayableAdmin):
    pass


class SectionAdmin(DisplayableAdmin):
    pass


admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
