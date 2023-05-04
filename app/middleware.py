import logging
import re
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from app.models import Chat, CHAT_SLUG_REGEX

User = get_user_model()


async def return_error(send, status: int, text: str):
    await send({
        'type': 'websocket.accept',
        'status': status,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'websocket.send',
        'text': text,
    })
    return await send({
        'type': 'websocket.close',
    })


class ChatMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        chat = None
        friend = None
        query_string = scope['query_string'].decode('utf-8')
        query_params = parse_qs(query_string)
        chat_slug = query_params.get('chat_slug', [None])[0]
        chat_id = query_params.get('chat_id', [None])[0]
        user_id = query_params.get('user_id', [None])[0]
        if chat_slug:
            if re.match(CHAT_SLUG_REGEX, chat_slug):
                try:
                    chat = await database_sync_to_async(Chat.objects.get)(slug=chat_slug, members=scope['user'])
                except Chat.DoesNotExist:
                    return await return_error(send, 404, _('Chat not found'))
            else:
                return await return_error(send, 400, _('Invalid chat slug'))
        elif chat_id:
            try:
                chat = await database_sync_to_async(Chat.objects.get)(id=chat_id, members=scope['user'])
            except Chat.DoesNotExist:
                return await return_error(send, 404, _('Chat not found'))
        elif user_id:
            try:
                friend = await database_sync_to_async(User.objects.get)(id=user_id)
            except User.DoesNotExist:
                return await return_error(send, 404, _('User not found'))
        else:
            return await return_error(send, 400, _('Invalid query params'))
        scope['chat'] = chat
        scope['friend'] = friend
        try:
            return await super().__call__(scope, receive, send)
        except Exception as e:
            logging.error(e)
            # TODO: handle all exceptions and return correct status code and message
            return await return_error(send, 503, _('Unavailable'))
