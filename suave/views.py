from django.http import Http404
from django.template.response import TemplateResponse

from djpjax import pjaxtend

from .utils import get_page_from_url


@pjaxtend()
def page(request, url='/'):
    """Show a page."""
    page = get_page_from_url(url)
    if page == False:
        raise Http404

    template = page.template_override
    if not template:
        template = 'page.html'
    return TemplateResponse(request, template, dict(
        page=page
    ))
