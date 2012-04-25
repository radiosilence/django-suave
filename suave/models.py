import re
from django.db import models
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from mptt.models import MPTTModel, TreeForeignKey

from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField

from tinymce import models as tinymce_models


class SiteEntityQuerySet(QuerySet):
    def live(self):
        return self.filter(status=SiteEntity.STATUS.live)


class SiteEntity(models.Model):
    STATUS = Choices(
        ('draft', 'Draft'),
        ('live', 'Live'),
        ('deleted', 'Deleted')
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    order = models.IntegerField(null=True, blank=True)
    status = StatusField()

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def __unicode__(self):
        return self.title


class Displayable(SiteEntity):
    body = tinymce_models.HTMLField()


class Section(SiteEntity):
    url_override = models.CharField(max_length=255, null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    @property
    def url(self):
        if self.url_override:
            if re.match(r'^(?:https?://)?(?:[\w]+\.)(?:\.?[\w]{2,})+$',
                self.url_override):
                return self.url_override
            else:
                # Todo: Make this more reliable for generating navigation based
                #       on sections.
                return '/' + self.url_override
        try:
            return self.pages.live()[0].url
        except IndexError:
            return "#"

    class Meta:
        ordering = ['order']


class Page(MPTTModel, Displayable):
    section = models.ForeignKey(Section, related_name='pages')

    template_override = models.CharField(max_length=255, null=True,
        blank=True)

    parent = TreeForeignKey('self', null=True, blank=True,
        related_name='children')

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    @property
    def url(self):
        kwargs = {}
        require_section_slug = False
        if self != self.section.pages.live()[0]:
            kwargs['page_slug'] = self.slug
            require_section_slug = True

        if self.section != Section.objects.live()[0] or \
            require_section_slug:
            kwargs['section_slug'] = self.section.slug

        return reverse('suave:page', kwargs=kwargs)

    class Meta:
        ordering = ['order']
