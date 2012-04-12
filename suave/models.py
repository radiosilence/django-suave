import re
from django.db import models
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse

from model_utils import Choices
from model_utils.managers import PassThroughManager


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
    sort_index = models.IntegerField()
    status = models.CharField(choices=STATUS, default=STATUS.draft,
        max_length=20)

    objects = PassThroughManager.for_queryset_class(SiteEntityQuerySet)()

    def __unicode__(self):
        return self.title


class Displayable(SiteEntity):
    body = models.TextField()


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
        ordering = ['sort_index']


class Page(Displayable):
    section = models.ForeignKey(Section, related_name='pages')
    featured_image = models.CharField(max_length=255, null=True,
        blank=True)
    featured_image_description = models.CharField(max_length=255, null=True,
        blank=True)

    template_override = models.CharField(max_length=255, null=True,
        blank=True)

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
        ordering = ['sort_index']
