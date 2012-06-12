from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import Page, Carousel, CarouselImage, Attachment, Nav, NavItem, \
    Redirect


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ['order']
    list_display = ['order']

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'admin/js/list-reorder.js',
            'admin/js/inline-reorder.js',
        )


class SiteEntityAdmin(reversion.VersionAdmin, OrderedAdmin):
    list_editable = ['order', 'status']
    list_display = ['title', 'status', 'order']
    list_filter = ['status']
    search_fields = ['title']


class DisplayableAdmin(SiteEntityAdmin):
    list_display = ['title', 'slug', 'status', 'order']
    prepopulated_fields = {"slug": ("title",)}


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    list_display = ['title', 'url', 'status', 'order']
    exclude = ['url']

admin.site.register(Page, PageAdmin)


class AttachmentAdmin(SiteEntityAdmin):
    pass

admin.site.register(Attachment, AttachmentAdmin)


class NavItemInline(admin.TabularInline):
    model = NavItem
    extra = 0


class NavAdmin(SiteEntityAdmin):
    inlines = [
        NavItemInline
    ]

admin.site.register(Nav, NavAdmin)


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage


class CarouselAdmin(admin.ModelAdmin):
    inlines = [
        CarouselImageInline
    ]


admin.site.register(Carousel, CarouselAdmin)


class RedirectAdmin(OrderedAdmin):
    list_display = ['old_url', 'new_url', 'order']

admin.site.register(Redirect, RedirectAdmin)
