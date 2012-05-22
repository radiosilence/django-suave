from copy import copy
from django.db import models
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from sorl.thumbnail import ImageField
from tinymce import models as tinymce_models


class SiteEntityQuerySet(QuerySet):
    def live(self):
        return self.filter(status=SiteEntity.STATUS.live)


class SiteEntity(models.Model):
    STATUS = Choices(
        ('draft', 'Draft'),
        ('live', 'Live'),
    )

    title = models.CharField(max_length=255)
    identifier = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = StatusField()

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

        return super(SiteEntity, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order']
        abstract = True


class Displayable(SiteEntity):
    body = tinymce_models.HTMLField(null=True, blank=True)
    slug = models.SlugField(max_length=255)

    class Meta:
        ordering = ['order']
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


class Page(MPTTModel, Displayable):
    template_override = models.CharField(max_length=255, null=True,
        blank=True)

    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')
    url = models.CharField(max_length=255, null=True, blank=True)
    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def save(self, *args, **kwargs):
        old_url = copy(self.url)
        self.update_url()

        super(Page, self).save(*args, **kwargs)

        if self.url != old_url:
            for child in self.get_children().all():
                child.save()

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


class Carousel(SiteEntity):
    pass


class CarouselImage(models.Model):
    carousel = models.ForeignKey(Carousel)
    image = ImageField(upload_to='carousel_img')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)


class Nav(SiteEntity):
    items = models.ManyToManyField(Page, related_name='navs',
        through='NavItem')


class NavItem(models.Model):
    page = models.ForeignKey(Page, related_name='navitems')
    nav = models.ForeignKey(Nav, related_name='navitems')
    show_children = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    @property
    def show_id(self):
        return self.pk

    def __unicode__(self):
        return unicode(self.page)

    class Meta:
        ordering = ['order']
