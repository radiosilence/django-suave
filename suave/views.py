from django.http import Http404
from django.template.response import TemplateResponse

from djpjax import pjaxtend

from .models import Page, Section


@pjaxtend()
def page(request, section_slug=None, page_slug=None):
    """Show a page."""
    print section_slug, page_slug
    try:
        if section_slug:
            section = Section.objects.filter(live=True).get(slug=section_slug)
        else:
            section = Section.objects.filter(live=True)[0]

        if page_slug:
            page = section.pages.get(slug=page_slug)
        else:
            page = section.pages.filter(live=True)[0]

        if page.template_override:
            template = page.template_override
        else:
            template = 'page.html'
    

    except (Page.DoesNotExist, Section.DoesNotExist, IndexError):
        raise Http404

    return TemplateResponse(request, template, dict(
        page=page,
        section=section,
        nav_secondary=section.pages.filter(live=True).all(),
        nav_secondary_selected=page
    ))