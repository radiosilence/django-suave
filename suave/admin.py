from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import (Page, ImageCarousel, ImageCarouselImage,
    NavItem, Redirect, Image, Attachment, PageContent)


class SuaveAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery.badmanforms.js',
        )


class DatedAdmin(SuaveAdmin):
    pass


class OrderedAdmin(SuaveAdmin):
    list_editable = ('order',)
    list_display = DatedAdmin.list_display + ('order',)
    exclude = ('order',)

    class Media:
        js = SuaveAdmin.Media.js + (
            'js/jquery-ui.min.js',
            'admin/js/list-reorder.js',
            'admin/js/inline-reorder.js',
        )

class OrderedInline(admin.TabularInline):
    class Media:
        js = SuaveAdmin.Media.js + OrderedAdmin.Media.js


class SiteEntityAdmin(SuaveAdmin, reversion.VersionAdmin):
    list_editable = ('status', )
    list_display = ('title', 'status')
    list_filter = ('status',)
    exclude = ('identifier',)
    search_fields = ('title',)

    Media = SuaveAdmin.Media


class OrderedEntityAdmin(SiteEntityAdmin):
    list_editable = SiteEntityAdmin.list_editable + OrderedAdmin.list_editable
    list_display = DatedAdmin.list_display + ('status', 'order',)
    exclude = SiteEntityAdmin.exclude + OrderedAdmin.exclude

    Media = OrderedAdmin.Media


class DisplayableAdmin(SiteEntityAdmin):
    list_display = ('title', 'slug', 'status')
    prepopulated_fields = {"slug": ("title",)}


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    list_display = ('title', 'url', 'status')
    exclude = ('url',)

admin.site.register(Page, PageAdmin)


class NavItemAdmin(SuaveAdmin, MPTTModelAdmin):
    list_display = ('title', 'url', 'type')
    mptt_indent_field = "title"

admin.site.register(NavItem, NavItemAdmin)


class ImageCarouselImageInline(admin.TabularInline):
    model = ImageCarouselImage


class ImageCarouselAdmin(admin.ModelAdmin):
    inlines = [
        ImageCarouselImageInline
    ]


admin.site.register(ImageCarousel, ImageCarouselAdmin)


class RedirectAdmin(OrderedAdmin):
    list_display = ('old_url', 'new_url', 'order')


class ImageInline(OrderedInline):
    model = Image
    fields = ('admin_thumbnail', 'image', 'alt', 'title', 'credit', 'order')
    readonly_fields = ('admin_thumbnail', )


class AttachmentInline(OrderedInline):
    model = Attachment
    fields = ('file', 'order')


admin.site.register(Redirect, RedirectAdmin)


class PageContentAdmin(SiteEntityAdmin):
    exclude = ()

admin.site.register(PageContent, PageContentAdmin)