import babylon

from django.http import Http404


def rendered_page_or_404(request, url=None):
    if not url:
        url = request.path
    pjax = request.GET.get('HTTP_X_PJAX', False)
    content = babylon.get('RenderedPageCache', url, pjax, request=request)
    if not content:
        raise Http404
    return content

def get_page_or_404(request, url=None):
    if not url:
        url = request.path
    page = babylon.get('PageCache', url)
    if not page:
        raise Http404
    return page
