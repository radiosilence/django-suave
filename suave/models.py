import mimetypes
import os

import django.dispatch

from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from sorl.thumbnail import ImageField
from sorl.thumbnail.helpers import ThumbnailError
from sorl.thumbnail import get_thumbnail

from tinymce import models as tinymce_models


class Dated(models.Model):
    """Mixin provides added/updated time to a model"""
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Ordered(models.Model):
    """Mixin provides ordering features to a model."""
    order = models.IntegerField(null=True, blank=True, db_index=True,
        verbose_name=_('display order'))

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.order is None:
            # Append
            try:
                last = model.objects.order_by('-order')[0]
                last_order = last.order
                if not last_order:
                    last_order = model.objects.all().count()
                self.order = last_order
            except IndexError:
                # First row
                self.order = 0

        super(Ordered, self).save(*args, **kwargs)

    class Meta:
        ordering = ('order', )
        abstract = True


class SiteEntityQuerySet(QuerySet):
    def live(self):
        return self.filter(status=SiteEntity.STATUS.live)


class SiteEntity(Dated):
    """Base model for entity which can be live/draft and has title, identifier,
    and status. Also provides a queryset .live()."""

    STATUS = Choices(
        ('draft', 'Draft'),
        ('live', 'Live'),
    )

    title = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, null=True, blank=True)
    status = StatusField(db_index=True)

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class MetaInfo(models.Model):
    """Mixin provides meta tags and page title (for SEO) with heirarchical 
    resolution for pages."""

    _page_title = models.CharField(max_length=255, blank=True, null=True,
        verbose_name="Page Title", help_text='This will override the "title"'
            + ' value and corresponds to the &lt;title&gt; tag of the page.')

    _meta_keywords = models.TextField(blank=True, null=True,
        verbose_name=_("Meta Keywords"))
    _meta_description = models.TextField(blank=True, null=True,
        verbose_name=_("Meta Description"), help_text='max 156 characters')

    @property
    def page_title(self):
        """Returns meta page title, or own title."""
        return self._page_title or self.title

    def meta_keywords():
        """Returns heirarchically resolved meta keywords."""
        def fget(self):
            if self._meta_keywords:
                return self._meta_keywords
            try:
                if self.parent:
                    return self.parent.meta_keywords
            except AttributeError:
                pass

            try:
                if hasattr(self, 'url'):
                    if self.url == '/':
                        return False
                return Page.objects.get(url='/').meta_keywords
            except Page.DoesNotExist:
                return False

        def fset(self, value):
            self._meta_keywords = value

        def fdel(self):
            del self._meta_keywords
        return locals()
    meta_keywords = property(**meta_keywords())

    def meta_description():
        """Returns heirarchically resolved meta description."""
        def fget(self):
            if self._meta_description:
                return self._meta_description
            try:
                if self.parent:
                    return self.parent.meta_description
            except AttributeError:
                pass

            try:
                if hasattr(self, 'url'):
                    if self.url == '/':
                        return False
                return Page.objects.get(url='/').meta_description
            except Page.DoesNotExist:
                return False

        def fset(self, value):
            self._meta_description = value

        def fdel(self):
            del self._meta_description
        return locals()
    meta_description = property(**meta_description())

    class Meta:
        abstract = True


class Displayable(SiteEntity):
    """Base type for page."""

    body = tinymce_models.HTMLField(null=True, blank=True,
        verbose_name=_('content'))
    slug = models.SlugField(max_length=255, db_index=True,
        help_text='The slug is the part of the URL distinct to this item '
            + '(eg. if our item was a potato and the URL was /vegetables/'
            + 'potato, the slug would be "potato"). Usually it is just a '
            + 'simplified, lower case version of the item name. It is also '
            + 'automatically generated by default.')

    class Meta:
        abstract = True


class Page(MPTTModel, Displayable, MetaInfo):
    """A normal page."""
    template_override = models.CharField(max_length=255, null=True,
        blank=True)

    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')
    url = models.CharField(max_length=255, null=True, blank=True)

    # Because we're not directly inheriting from Displayable, we need to make
    # sure the default manager is set.
    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def update_url(self, save=True):
        self.url = self._url

    @property
    def _url(self):
        if self.is_root_node():
            return reverse('suave:page')

        url = '{0}{1}/'.format(
            self.parent.url,
            self.slug
        )
        return url

    def get_absolute_url(self):
        return self.url


Page._meta.get_field('body').verbose_name = _('page content')


@receiver(pre_save, sender=Page)
def page_url_update(sender, instance, **kwargs):
    instance.old_url = instance.url
    instance.update_url()


@receiver(post_save, sender=Page)
def page_child_url_update(sender, instance, **kwargs):
    if instance.old_url != instance.url:
        for child in instance.get_children().all():
            child.save()


class ImageCarousel(SiteEntity):
    pass


class ImageCarouselImage(models.Model):
    carousel = models.ForeignKey(ImageCarousel)
    image = ImageField(upload_to='carousel_img')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)


class NavItem(MPTTModel, Dated):
    TYPE = Choices(
        ('menu', 'Menu'),
        ('page', 'Page'),
        ('dynamic', 'Dynamic'),
        ('static', 'Static')
    )
    type = models.CharField(max_length=15, choices=TYPE, default=TYPE.menu)
    text = models.CharField(max_length=127, blank=True, null=True)
    template = models.CharField(max_length=255, blank=True, null=True)

    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')

    page = models.ForeignKey(Page, related_name='navitems', null=True,
        blank=True)
    page_show_children = models.BooleanField(default=True)

    dynamic_name = models.CharField(max_length=255, blank=True, null=True)
    dynamic_args = models.TextField(blank=True, null=True)

    static_url = models.CharField(max_length=255, blank=True, null=True)

    def active(self, path, exact=True):
        if exact:
            return path == self.url
        else:
            return path.startswith(self.url)

    @property
    def ordered_children(self):
        return self.children.order_by('order')

    @property
    def url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        if self.type == NavItem.TYPE.page:
            return self.page.url
        elif self.type == NavItem.TYPE.dynamic:
            args = {}
            for arg in self.dynamic_args.split(';'):
                try:
                    k, v = arg.split(':')
                    args[k] = v
                except ValueError:
                    pass
            try:
                return reverse(self.dynamic_name, kwargs=args)
            except:
                return '#'
        elif self.type == NavItem.TYPE.menu:
            try:
                return self.get_children()[0].url
            except IndexError:
                return '#'
        elif self.type == NavItem.TYPE.static:
            return self.static_url

    @property
    def title(self):
        if not self.text and self.type == NavItem.TYPE.page:
            return self.page.title
        elif self.text:
            return self.text
        else:
            return 'Nav Item #{}'.format(self.id)

    @property
    def navs(self):
        subitems = self.get_children()
        if self.type == NavItem.TYPE.page:
            subitems.extend(self.page.children.live())

    def __unicode__(self):
        return u'{}'.format(self.title)


class Attachment(Ordered):
    file = models.FileField(upload_to='uploads')

    @property
    def filename(self):
        return self.file.name.split('/')[-1]

    @property
    def size(self):
        num = self.file.size
        s = '{0:.{2}f}{1}'
        p = 0
        for x in [' bytes','KB','MB','GB', 'TB']:
            if num < 1024.0:
                return s.format(num, x, p)
            num /= 1024.0
            p = 2
        return s.format(num, 'PB')

    @property
    def icon(self):
        def filename(mimetype):
            try:
                return '{}{}.png'.format(
                    settings.ICON_PATH,
                    mimetype.replace('/', '-') 
                )
            except AttributeError:
                return None

        filetype, _ = mimetypes.guess_type(self.filename)
        if not filetype or \
            not os.path.exists(settings.STATIC_ROOT + filename(filetype)):
            filetype = 'empty'
            
        return filename(filetype)

    class Meta:
        abstract = True
        ordering = ('order',)


class Redirect(Ordered):
    old_url = models.CharField(max_length=255)
    new_url = models.CharField(max_length=255, blank=True)
    permanent = models.BooleanField(default=True)


class Image(Ordered):
    image = ImageField(upload_to='uploads')
    alt = models.CharField(max_length=511, null=True, blank=True)
    title = models.CharField(max_length=511, null=True, blank=True)
    credit = models.CharField(max_length=255, null=True, blank=True)

    @property
    def admin_thumbnail(self):
        try:
            return mark_safe('<img src="{}"/>'.format(
                get_thumbnail(self.image, '160x90', crop='center',
                    quality=100).url
            ))
        except (IOError, ThumbnailError):
            return ''

    def __str__(self):
        return mark_safe(self.image.url)

    class Meta:
        abstract = True
        ordering = ('order',)


pre_route = django.dispatch.Signal(providing_args=['url'])
post_route = django.dispatch.Signal(providing_args=['url'])


class ContentBlock(SiteEntity):
    body = tinymce_models.HTMLField(null=True, blank=True)

    class Meta:
        abstract = True

class PageContent(ContentBlock):
    page = models.ForeignKey(Page, null=True, blank=True,
        related_name='content')

    class Meta:
        verbose_name = 'block of page content'
        verbose_name_plural = 'blocks of page content'


from .caches import *
