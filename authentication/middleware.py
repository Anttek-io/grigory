import datetime

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.security.websocket import WebsocketDenier

from authentication.models import Token
from core.settings import REST_AUTH_TOKEN_TTL


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
    except Token.DoesNotExist:
        return None
    else:
        if not token.user.is_active:
            return None
        if not token.active:
            return None
        now = datetime.datetime.now()
        diff = now - datetime.timedelta(seconds=REST_AUTH_TOKEN_TTL)
        if token.last_use < diff:
            token.active = False
            token.save()
            return None
    token.last_use = now
    token.save()
    return token.user


class TokenAuthMiddleware(BaseMiddleware):
    """
    Token authorization middleware for Django Channels 4.
    Parses the token from the connection's headers and populates
    scope["user"]. If the token is invalid, denies the connection.
    """
    keyword = 'Bearer'

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            auth = headers[b"authorization"].decode()
            if auth.startswith(self.keyword):
                token = auth.split()[1]
                scope["user"] = await get_user(token)
        if not scope.get('user'):
            denier = WebsocketDenier()
            return await denier(scope, receive, send)
        return await super().__call__(scope, receive, send)
