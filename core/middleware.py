from django.http import HttpResponse
from channels.middleware import BaseMiddleware


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/health':
            return HttpResponse('ok')
        return self.get_response(request)


class WebSocketHealthCheckMiddleware(BaseMiddleware):
    """
    Health check middleware for Django Channels 4.
    """
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        is_health_check = scope['path'].split('/')[-1] == 'health'
        if is_health_check:
            # Accept the connection
            await send({
                "type": "websocket.accept",
            })
            # Send a message down the channel
            await send({
                "type": "websocket.send",
                "text": "ok",
            })
            # Close the connection
            await send({
                "type": "websocket.close",
            })
            return
        return await super().__call__(scope, receive, send)
