from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import (Page, ImageCarousel, ImageCarouselImage, Attachment, Nav,
    NavItem, Redirect, Image, PageContent)


class DatedAdmin(admin.ModelAdmin):
    pass

class OrderedAdmin(DatedAdmin):
    list_editable = ('order',)
    list_display = DatedAdmin.list_display + ('order',)
    exclude = ('order',)

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'admin/js/list-reorder.js',
            'admin/js/inline-reorder.js',
        )


class SiteEntityAdmin(reversion.VersionAdmin, OrderedAdmin):
    list_editable = ('order', 'status')
    list_display = ('title', 'status', 'order')
    list_filter = ('status',)
    exclude = OrderedAdmin.exclude + ('identifier',)
    search_fields = ('title',)


class DisplayableAdmin(SiteEntityAdmin):
    list_display = ('title', 'slug', 'status', 'order')
    prepopulated_fields = {"slug": ("title",)}


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    list_display = ('title', 'url', 'status', 'order')
    exclude = ('url',)

admin.site.register(Page, PageAdmin)


class AttachmentAdmin(SiteEntityAdmin):
    pass

admin.site.register(Attachment, AttachmentAdmin)


class NavItemAdmin(MPTTModelAdmin, OrderedAdmin):
    list_display = ('title', 'url', 'type', 'order')
    mptt_indent_field = "title"

admin.site.register(NavItem, NavItemAdmin)


class ImageCarouselImageInline(admin.TabularInline):
    model = CarouselImage


class ImageCarouselAdmin(admin.ModelAdmin):
    inlines = [
        CarouselImageInline
    ]


admin.site.register(ImageCarousel, ImageCarouselAdmin)


class RedirectAdmin(OrderedAdmin):
    list_display = ('old_url', 'new_url', 'order')


class ImageInline(admin.TabularInline):
    model = Image
    fields = ('admin_thumbnail', 'image', 'alt', 'order')
    readonly_fields = ('admin_thumbnail', )


admin.site.register(Redirect, RedirectAdmin)


class PageContentAdmin(SiteEntityAdmin):
    exclude = OrderedAdmin.exclude

admin.site.register(PageContent, PageContentAdmin)