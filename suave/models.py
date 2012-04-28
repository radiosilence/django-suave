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
    slug = models.SlugField(max_length=255)
    order = models.IntegerField(null=True, blank=True)
    status = StatusField()

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['order', 'title']


class Displayable(SiteEntity):
    body = tinymce_models.HTMLField()


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

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    @property
    def url(self):
        if self.is_root_node():
            return reverse('suave:page')

        crumbs = []
        for ancestor in self.get_ancestors():
            if ancestor.is_root_node():
                continue
            crumbs.append(ancestor.slug)
        crumbs.append(self.slug)
        return reverse('suave:page', kwargs=dict(
            url='/'.join(crumbs)))

    class Meta:
        ordering = ['order']


class Carousel(models.Model):
    name = models.CharField(max_length=45, unique=True)
    images = models.ManyToManyField(Attachment, related_name='carousels',
        through='CarouselImage')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class CarouselImage(models.Model):
    image = models.ForeignKey(Attachment)
    carousel = models.ForeignKey(Carousel)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
