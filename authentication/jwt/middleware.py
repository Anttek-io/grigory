import logging

from channels.auth import login, AuthMiddleware
from channels.db import database_sync_to_async
from channels.security.websocket import WebsocketDenier
from channels.sessions import CookieMiddleware, SessionMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

from core.settings import SECRET_KEY


class TokenAuthMiddleware:
    keyword = 'Bearer'

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope.get('user') not in (None, AnonymousUser):
            return await self.inner(scope, receive, send)
        close_old_connections()
        headers = dict(scope["headers"])
        if b"authorization" in headers:
            auth = headers[b"authorization"].decode()
            if auth.startswith(self.keyword):
                token = auth.split()[1]
                try:
                    UntypedToken(token)
                except (InvalidToken, TokenError) as e:
                    logging.error(e)
                    denier = WebsocketDenier()
                    return await denier(scope, receive, send)
                else:
                    decoded_data = jwt_decode(token, SECRET_KEY, algorithms=["HS256"])
                    defaults = decoded_data["user"]
                    user, user_created = await database_sync_to_async(get_user_model().objects.update_or_create)(
                        id=decoded_data["user_id"],
                        defaults=defaults
                    )
                    await login(scope, user)
                    scope["user"] = user
        return await self.inner(scope, receive, send)


def AuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(AuthMiddleware(inner))))
