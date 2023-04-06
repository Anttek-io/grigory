from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from app.models import Chat


class ChatMiddleware(BaseMiddleware):
    """
    Parse the query string for one of the following:
    - chat_slug: the slug of the chat
    - chat_id: the id of the chat
    Pass the chat_id to the scope.
    If chat_slug is passed but Chat does not exist, create it.
    If chat_id is passed but Chat does not exist, return 404.
    """

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode('utf-8')
        query_params = parse_qs(query_string)
        chat_slug = query_params.get('chat_slug', [None])[0]
        chat_id = query_params.get('chat_id', [None])[0]
        if chat_slug:
            chat, _ = await database_sync_to_async(Chat.objects.get_or_create)(slug=chat_slug)
        elif chat_id:
            try:
                chat = await database_sync_to_async(Chat.objects.get)(id=chat_id)
            except Chat.DoesNotExist:
                await send({
                    'type': 'websocket.accept',
                    'status': 404,
                    'headers': [
                        [b'content-type', b'text/plain'],
                    ],
                })
                await send({
                    'type': 'websocket.send',
                    'text': 'Chat does not exist',
                })
                return await send({
                    'type': 'websocket.close',
                })
        else:
            await send({
                'type': 'websocket.accept',
                'status': 400,
                'headers': [
                    [b'content-type', b'text/plain'],
                ],
            })
            await send({
                'type': 'websocket.send',
                'text': 'chat_slug or chat_id is required',
            })
            return await send({
                'type': 'websocket.close',
            })
        scope['chat'] = chat
        return await super().__call__(scope, receive, send)
