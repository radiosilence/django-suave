from .models import pre_route


class PreRouteMiddleWare(object):
    def process_view(self, request, *args, **kwargs):
        pre_routes = pre_route.send(sender=request, url=request.path)
        for reciever, response in pre_routes:
            if response:
                return response
        return None
