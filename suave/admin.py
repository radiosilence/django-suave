from django.contrib import admin

from .models import Page, Section


class DisplayableAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class PageAdmin(DisplayableAdmin):
    pass


class SectionAdmin(DisplayableAdmin):
    pass


admin.site.register(Page, PageAdmin)
admin.site.register(Section, SectionAdmin)
