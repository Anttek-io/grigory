import datetime

from channels.auth import login, AuthMiddleware
from channels.db import database_sync_to_async
from channels.security.websocket import WebsocketDenier
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

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
        now = timezone.now()
        diff = now - datetime.timedelta(seconds=REST_AUTH_TOKEN_TTL)
        if token.last_use < diff:
            token.active = False
            token.save()
            return None
    token.last_use = now
    token.save()
    return token.user


class TokenAuthMiddleware:
    keyword = 'Bearer'

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope.get('user') not in (None, AnonymousUser):
            return await self.inner(scope, receive, send)
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            auth = headers[b"authorization"].decode()
            if auth.startswith(self.keyword):
                token = auth.split()[1]
                scope["user"] = await get_user(token)
                if scope.get('user') not in (None, AnonymousUser):
                    await login(scope, scope.get('user'))
                else:
                    denier = WebsocketDenier()
                    return await denier(scope, receive, send)
        return await self.inner(scope, receive, send)


def AuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(AuthMiddleware(inner))))
