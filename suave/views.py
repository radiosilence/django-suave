from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect

from djpjax import pjaxtend

from .models import Redirect, pre_route, post_route
from .utils import get_page_from_url


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

            post_routes = post_route.send(sender=request, url=url)
            for reciever, response in post_routes:
                if response:
                    return response
            raise Http404

    template = page.template_override
    if not template:
        template = 'page.html'
    return TemplateResponse(request, template, dict(
        active=page,
        page=page
    ))
