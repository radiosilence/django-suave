from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import Page, Carousel, CarouselImage, Attachment


class SiteEntityAdmin(reversion.VersionAdmin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class DisplayableAdmin(SiteEntityAdmin):
    pass


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    pass

admin.site.register(Page, PageAdmin)


class AttachmentAdmin(SiteEntityAdmin):
    pass

admin.site.register(Attachment, AttachmentAdmin)


class AttachmentInline(admin.TabularInline):
    model = Attachment


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage


class CarouselAdmin(admin.ModelAdmin):
    inlines = [
        CarouselImageInline
    ]

admin.site.register(Carousel, CarouselAdmin)
