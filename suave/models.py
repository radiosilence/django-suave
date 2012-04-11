import re
from django.db import models
from django.core.urlresolvers import reverse


class Displayable(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    sort_index = models.IntegerField()
    live = models.BooleanField()


class Section(Displayable):
    url_override = models.CharField(max_length=255, null=True, blank=True)

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
            return self.pages.filter(live=True)[0].url
        except IndexError:
            return "#"

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort_index']


class Page(Displayable):
    content = models.TextField()
    section = models.ForeignKey(Section, related_name='pages')
    featured_image = models.CharField(max_length=255, null=True,
        blank=True)
    featured_image_description = models.CharField(max_length=255, null=True,
        blank=True)

    @property
    def url(self):
        if self.section == Section.objects.filter(live=True)[0]:
            section_slug = ''
        else:
            section_slug = self.section.slug

        if self == self.section.pages.filter(live=True)[0]:
            page_slug = ''
        else:
            page_slug = '/' + self.slug

        d = {}
        if section_slug:
            d['section_slug'] = section_slug
        if page_slug:
            d['page_slug'] = page_slug

        url = reverse('page', kwargs=d)
        return url

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort_index']
