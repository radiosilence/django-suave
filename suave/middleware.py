from .models import pre_route


class PreRouteMiddleWare(object):
    def process_request(self, request):
        url = request.path.strip('/')
        if url == '':
            url = '/'
        pre_routes = pre_route.send(sender=request, url=url)
        for reciever, response in pre_routes:
            if response:
                return response
        return None
