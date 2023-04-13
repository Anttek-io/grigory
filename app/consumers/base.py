import json
import logging

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from app.models import Message
from app.serializers.messages import MessageSerializer

MESSAGES_LIMIT = 10


def get_serializer_data(instance, many=False):
    serializer_class = MessageSerializer
    serializer = serializer_class(instance, many=many)
    return serializer.data


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat = None
        self.message = None

    async def create_message(self, message):
        return await database_sync_to_async(Message.objects.create)(
            chat=self.chat,
            text=message,
            sender_id=self.user.id
        )

    async def connect(self):
        self.user = self.scope['user']
        self.chat = self.scope['chat']
        await self.channel_layer.group_add(
            self.chat.slug,
            self.channel_name
        )
        await self.accept()
        await self.send_message_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat.slug,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return
        message = data.get('message')
        action = data.get('action')
        if action == 'load_messages':
            offset = data.get('offset', 0)
            limit = data.get('limit', MESSAGES_LIMIT)
            await self.send_message_list(offset, limit)
        if message:
            self.message = await self.create_message(message)
            data = {'type': 'message'}
            serializer_data = await sync_to_async(get_serializer_data)(self.message)
            data.update(serializer_data)
            await self.channel_layer.group_send(
                self.chat.slug,
                {
                    'type': 'chat_message',
                    'data': data
                }
            )

    async def chat_message(self, event):
        assert event.get('data'), 'Data is required'
        await self.send(text_data=json.dumps(event['data']))

    async def send_message_list(self, offset=0, limit=MESSAGES_LIMIT):
        messages, count, total = await self.get_messages(offset, limit)
        data = {
            'type': 'message_list',
            'offset': offset,
            'limit': limit,
            'count': count,
            'total': total,
            'messages': messages
        }
        await self.channel_layer.group_send(
            self.chat.slug,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    @database_sync_to_async
    def get_messages(self, offset=0, limit=MESSAGES_LIMIT):
        qs = Message.objects.filter(chat=self.chat).order_by('-timestamp')[offset:limit]
        total = Message.objects.filter(chat=self.chat).count()
        data = get_serializer_data(qs, many=True)
        return data, qs.count(), total
