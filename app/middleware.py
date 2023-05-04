import re
from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

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
                chat = await database_sync_to_async(Chat.objects.get)(slug=chat_slug)
            else:
                await return_error(send, 400, 'Invalid chat slug')
        elif chat_id:
            try:
                chat = await database_sync_to_async(Chat.objects.get)(id=chat_id)
            except Chat.DoesNotExist:
                await return_error(send, 404, 'Chat does not exist')
        elif user_id:
            try:
                friend = await database_sync_to_async(User.objects.get)(id=user_id)
            except User.DoesNotExist:
                await return_error(send, 404, 'User does not exist')
        else:
            await return_error(send, 400, 'No chat slug, chat id or user id provided')
        scope['chat'] = chat
        scope['friend'] = friend
        return await super().__call__(scope, receive, send)
