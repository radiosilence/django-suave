from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect

from djpjax import pjaxtend

from .models import Redirect
from .utils import get_page_from_url


@cache_page(60)
@pjaxtend()
def page(request, url='/'):
    """Show a page."""
    try:
        page = get_page_from_url(url)
    except Http404:
        try:
            r = Redirect.objects.get(old_url=url)
            return redirect(r.new_url, permanent=r.permanent)
        except Redirect.DoesNotExist:
            raise Http404

    template = page.template_override
    if not template:
        template = 'page.html'
    return TemplateResponse(request, template, dict(
        active=page,
        page=page
    ))
