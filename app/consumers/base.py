import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from app.models import Message
from app.serializers.messages import MessageSerializer


MESSAGES_LIMIT = 10


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.chat = None
        self.message = None

    async def connect(self):
        self.user = self.scope['user']
        self.chat = self.scope['chat']
        await self.channel_layer.group_add(
            self.chat.slug,
            self.channel_name
        )
        await self.accept()
        await self.send_messages()

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
            offset = data.get('offset')
            limit = data.get('limit')
            await self.send_messages(offset, limit)
        if message:
            self.message = await self.create_message(message)
            await self.message.send_to_websocket()

    async def chat_message(self, event):
        event.pop('type')
        await self.send(text_data=json.dumps(event))

    async def create_message(self, message):
        return await database_sync_to_async(Message.objects.create)(
            chat=self.chat,
            text=message,
            sender_id=self.user.id
        )

    async def send_messages(self, offset=0, limit=MESSAGES_LIMIT):
        messages = await self.get_messages(offset, limit)
        await self.send(text_data=json.dumps({
            'offset': offset,
            'limit': limit,
            'messages': messages
        }))

    @database_sync_to_async
    def get_messages(self, offset=0, limit=MESSAGES_LIMIT):
        qs = Message.objects.filter(chat=self.chat).order_by('-timestamp')[offset:limit]
        serializer = MessageSerializer(qs, many=True)
        return serializer.data
