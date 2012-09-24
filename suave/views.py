import babylon

from django.http import Http404, HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import redirect, get_object_or_404

from djpjax import pjaxtend

from .models import Redirect, pre_route, post_route, Page
from .shortcuts import get_page_or_404, rendered_page_or_404

def page(request, url='/'):
    """Show a page.""" 
    try:
        content = rendered_page_or_404(request, url=url)
        return HttpResponse(content, content_type='text/html')
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