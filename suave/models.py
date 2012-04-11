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
        kwargs = {}
        require_section_slug = False
        if self != self.section.pages.filter(live=True)[0]:
            kwargs['page_slug'] = self.slug
            require_section_slug = True

        if self.section != Section.objects.filter(live=True)[0] or \
            require_section_slug:
            kwargs['section_slug'] = self.section.slug

        return reverse('suave:page', kwargs=kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['sort_index']
