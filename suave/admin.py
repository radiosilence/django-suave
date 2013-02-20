from django.contrib import admin

from mptt.admin import MPTTModelAdmin
import reversion

from .models import (Page, ImageCarousel, ImageCarouselImage,
    NavItem, Image, Attachment, ContentBlock)


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
    exclude = ()
    search_fields = ('title',)

    Media = SuaveAdmin.Media


class OrderedEntityAdmin(SiteEntityAdmin):
    list_editable = SiteEntityAdmin.list_editable + OrderedAdmin.list_editable
    list_display = DatedAdmin.list_display + ('status', 'order',)
    exclude = SiteEntityAdmin.exclude + OrderedAdmin.exclude

    Media = OrderedAdmin.Media


class SluggedAdmin(SuaveAdmin):
    prepopulated_fields = {"slug": ("title",)}


class DisplayableAdmin(SiteEntityAdmin):
    list_display = ('title', 'slug', 'status')


class PageAdmin(MPTTModelAdmin, DisplayableAdmin):
    list_display = ('title', 'url', 'status')
    prepopulated_fields = {"slug": ("title",)}
    exclude = ('url',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'status', 'parent', 'body'),
        }),
        ('Header', {
            'classes': ('collapse grp-collapse grp-closed',),
            'fields': ('header_title', 'header_image', 'header_content'),
        }),
        ('Meta/SEO', {
            'classes': ('collapse grp-collapse grp-closed',),
            'fields': ('_page_title', '_meta_keywords', '_meta_description',
                '_page_h1'),
        }),
        ('Advanced', {
            'classes': ('collapse grp-collapse grp-closed',),
            'fields': ('template_override',)
        }),
    )


admin.site.register(Page, PageAdmin)


class NavItemAdmin(SuaveAdmin, MPTTModelAdmin):
    list_display = ('title', 'url', 'type')
    mptt_indent_field = "title"
    fieldsets = (
        (None, {
            'fields': ('type', 'text', 'parent'),
        }),
        ('Menu', {
            'fields': ('template',),
        }),
        ('Page', {
            'fields': ('page', 'page_show_children',),
        }),
        ('Dynamic', {
            'fields': ('dynamic_name', 'dynamic_args',),
        }),
        ('Static', {
            'fields': ('static_url',),
        }),
        ('Tweaks', {
            'classes': ('collapse grp-collapse grp-closed',),
            'fields': ('extra_classes', 'css_id'),
        }),
    )

admin.site.register(NavItem, NavItemAdmin)


class ImageCarouselImageInline(admin.TabularInline):
    model = ImageCarouselImage


class ImageCarouselAdmin(admin.ModelAdmin):
    inlines = [
        ImageCarouselImageInline
    ]


admin.site.register(ImageCarousel, ImageCarouselAdmin)


class ImageInline(OrderedInline):
    model = Image
    fields = ('admin_thumbnail', 'image', 'alt', 'title', 'credit', 'order')
    readonly_fields = ('admin_thumbnail', )


class AttachmentInline(OrderedInline):
    model = Attachment
    fields = ('file', 'order')



class ContentBlockAdmin(admin.ModelAdmin):
    exclude = ()

admin.site.register(ContentBlock, ContentBlockAdmin)
