import django.dispatch
from django.db import models
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from sorl.thumbnail import ImageField
from tinymce import models as tinymce_models


class Ordered(models.Model):
    order = models.IntegerField(null=True, blank=True, db_index=True,
        verbose_name=_('display order'))
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        abstract = True


class SiteEntityQuerySet(QuerySet):
    def live(self):
        return self.filter(status=SiteEntity.STATUS.live)


class SiteEntity(Ordered):
    STATUS = Choices(
        ('draft', 'Draft'),
        ('live', 'Live'),
    )

    title = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, null=True, blank=True)
    status = StatusField(db_index=True)

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def save(self, *args, **kwargs):
        model = self.__class__

        if self.order is None:
            # Append
            try:
                last = model.objects.order_by('-order')[0]
                self.order = last.order + 1
            except IndexError:
                # First row
                self.order = 0

        super(SiteEntity, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class MetaInfo(models.Model):
    _page_title = models.CharField(max_length=255, blank=True, null=True,
        verbose_name="Page Title", help_text='This will override the "title"'
            + ' value and corresponds to the &lt;title&gt; tag of the page.')

    _meta_keywords = models.TextField(blank=True, null=True,
        verbose_name=_("Meta Keywords"))
    _meta_description = models.TextField(blank=True, null=True,
        verbose_name=_("Meta Description"), help_text='max 156 characters')

    @property
    def page_title(self):
        if self._page_title:
            return self._page_title
        else:
            return self.title

    def meta_keywords():
        def fget(self):
            if self._meta_keywords:
                return self._meta_keywords
            try:
                if self.parent:
                    return self.parent.meta_keywords
            except AttributeError:
                pass

            try:
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
        def fget(self):
            if self._meta_description:
                return self._meta_description
            try:
                if self.parent:
                    return self.parent.meta_description
            except AttributeError:
                pass

            try:
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
    body = tinymce_models.HTMLField(null=True, blank=True)
    slug = models.SlugField(max_length=255, db_index=True)

    class Meta:
        abstract = True


class Attachment(SiteEntity):
    TYPE = Choices(
        ('image', 'Image'),
        ('video', 'Video'),
        ('misc', 'Miscellaneous')
    )
    type = models.CharField(max_length=45, choices=TYPE, default=TYPE.image)
    image = ImageField(upload_to='uploads', null=True, blank=True)
    file = models.FileField(upload_to='uploads', null=True, blank=True)


class Page(MPTTModel, Displayable, MetaInfo):
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

    class Meta:
        ordering = ['order']


@receiver(pre_save, sender=Page)
def page_url_update(sender, instance, **kwargs):
    instance.old_url = instance.url
    instance.update_url()


@receiver(post_save, sender=Page)
def page_child_url_update(sender, instance, **kwargs):
    if instance.old_url != instance.url:
        for child in instance.get_children().all():
            child.save()


class Carousel(SiteEntity):
    pass


class CarouselImage(models.Model):
    carousel = models.ForeignKey(Carousel)
    image = ImageField(upload_to='carousel_img')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)


class Nav(SiteEntity):
    pass


class NavItem(MPTTModel, Ordered):
    TYPE = Choices(
        ('menu', 'Menu'),
        ('page', 'Page'),
        ('dynamic', 'Dynamic'),
        ('static', 'Static')
    )
    type = models.CharField(max_length=15, choices=TYPE, default=TYPE.menu)
    text = models.CharField(max_length=127, blank=True, null=True)

    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')

    page = models.ForeignKey(Page, related_name='navitems', null=True,
        blank=True)
    page_show_children = models.BooleanField(default=True)

    dynamic_name = models.CharField(max_length=255, blank=True, null=True)
    dynamic_args = models.TextField(blank=True, null=True)

    static_url = models.CharField(max_length=255, blank=True, null=True)

    @property
    def url(self):
        if self.type == NavItem.TYPE.page:
            return self.page.url
        elif self.type == NavItem.TYPE.dynamic:
            args = {}
            for arg in self.dynamic_args.split(';'):
                k, v = arg.split(':')
                args[k] = v
            try:
                return reverse(self.dynamic_name, kwargs=args)
            except:
                return '#'
        else:
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

    class Meta:
        ordering = ['order']


class Redirect(Ordered):
    old_url = models.CharField(max_length=255)
    new_url = models.CharField(max_length=255, blank=True)
    permanent = models.BooleanField(default=True)


class Image(Ordered):
    image = ImageField(upload_to='uploads')
    alt = models.CharField(max_length=511, null=True, blank=True)

    class Meta:
        abstract = True


pre_route = django.dispatch.Signal(providing_args=['url'])
post_route = django.dispatch.Signal(providing_args=['url'])
