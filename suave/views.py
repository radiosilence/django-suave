from jimmypage.cache import cache_page

from django.http import Http404
from django.shortcuts import redirect, get_object_or_404, render

from .models import pre_route, post_route, Page


@cache_page
def page(request, url='/'):
    """Show a page.""" 
    try:
        def fix_url(url):
            if url[-1] != '/':
               url = url + '/'

            if url[0] != '/':
               url = '/' + url
            return url

        url = fix_url(url)
        page = get_object_or_404(Page, url=url)

        template = page.template_override
        if not template:
           template = 'page.html'
        return render(request, template, {
            'active': page,
            'page': page,
        }, content_type='text/html')
    except Http404:
        post_routes = post_route.send(sender=request, url=url)
        for reciever, response in post_routes:
            if response:
                return response
        raise Http404