from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page

from djpjax import pjaxtend

from .utils import get_page_from_url


@cache_page(60)
@pjaxtend()
def page(request, url='/'):
    """Show a page."""
    page = get_page_from_url(url)
    template = page.template_override
    if not template:
        template = 'page.html'
    return TemplateResponse(request, template, dict(
        active=page,
        page=page
    ))
