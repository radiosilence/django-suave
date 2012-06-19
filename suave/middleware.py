from .models import pre_route


class PreRouteMiddleWare(object):
    def process_view(self, request, *args, **kwargs):
        url = request.path.strip('/')
        if url == '':
            url = '/'
        pre_routes = pre_route.send(sender=request, url=url)
        for reciever, response in pre_routes:
            if response:
                return response
        return None
