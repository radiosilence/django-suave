from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import Page, Carousel, CarouselImage, Attachment, Nav, NavItem


class SiteEntityAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ['order', 'status']
    list_display = ['title', 'slug', 'status', 'order']
    list_filter = ['status']
    search_fields = ['title']

    class Media:
        js = (
            'js/jquery.min.js',
            'js/jquery-ui.min.js',
            'admin/js/list-reorder.js',
            'admin/js/inline-reorder.js',
        )


class DisplayableAdmin(SiteEntityAdmin):
    pass


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    pass

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
