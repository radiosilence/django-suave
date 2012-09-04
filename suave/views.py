from django.http import Http404, HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect, get_object_or_404

import babylon

from djpjax import pjaxtend

from .models import Redirect, pre_route, post_route, Page


def page(request, url='/'):
    """Show a page.""" 
    def fix_url(url):
        if url[-1] != '/':
            url = url + '/'

        if url[0] != '/':
            url = '/' + url
        return url

    try:
        url = fix_url(url)
        page = babylon.get('PageCache', url)
        template = page.template_override
        if not template:
            template = 'page.html'

        parent = 'base.html'
        if request.GET.get('HTTP_X_PJAX', False):
            parent = 'pjax.html'

        return TemplateResponse(request, template, {
            'active': page,
            'page': page,
            'parent': parent
        })
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