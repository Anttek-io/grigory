import json
import re
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from app.models import Message, Chat, CHAT_TYPE_PRIVATE, CHAT_SLUG_REGEX
from app.serializers.messages import MessageSerializer

MESSAGES_LIMIT = 10

User = get_user_model()


def get_serializer_data(instance, many=False):
    serializer_class = MessageSerializer
    serializer = serializer_class(instance, many=many)
    return serializer.data


class ConversationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.chat = None
        self.friend = None
        self.user = None
        self.message = None
        self.group_name = None
        self.group_args = None

    async def create_message(self, message):
        if not self.chat and self.friend:
            self.chat = await database_sync_to_async(Chat.objects.create)(chat_type=CHAT_TYPE_PRIVATE,
                                                                          creator=self.user)
            await database_sync_to_async(self.chat.members.add)(self.user)
            if self.user != self.friend:
                await database_sync_to_async(self.chat.members.add)(self.friend)
            await self.switch_group(f'chat_{self.chat.id}')
        return await database_sync_to_async(Message.objects.create)(
            chat=self.chat,
            text=message,
            sender_id=self.user.id
        )

    async def return_error(self, status: int, text: str):
        await self.accept()
        await self.send(text_data=json.dumps({
            'status': status,
            'error': str(text)
        }))
        await self.close()

    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}'
        self.group_args = (self.group_name, self.channel_name)
        await self.channel_layer.group_add(*self.group_args)
        query_string = self.scope['query_string'].decode('utf-8')
        query_params = parse_qs(query_string)
        chat_slug = query_params.get('chat_slug', [None])[0]
        chat_id = query_params.get('chat_id', [None])[0]
        user_id = query_params.get('user_id', [None])[0]
        if chat_slug:
            if re.match(CHAT_SLUG_REGEX, chat_slug):
                try:
                    self.chat = await database_sync_to_async(Chat.objects.get)(slug=chat_slug, members=self.user)
                except Chat.DoesNotExist:
                    return await self.return_error(404, _('Chat not found'))
            else:
                return await self.return_error(400, _('Invalid chat slug'))
        elif chat_id:
            try:
                self.chat = await database_sync_to_async(Chat.objects.get)(id=chat_id, members=self.user)
            except Chat.DoesNotExist:
                return await self.return_error(404, _('Chat not found'))
        elif user_id:
            try:
                self.friend = await database_sync_to_async(User.objects.get)(id=user_id)
            except User.DoesNotExist:
                return await self.return_error(404, _('User not found'))
        else:
            return await self.return_error(400, _('Invalid query params'))
        if not self.chat and self.friend:
            try:
                self.chat = await database_sync_to_async(self.user.chats.get)(members=self.friend,
                                                                              chat_type=CHAT_TYPE_PRIVATE)
            except Chat.DoesNotExist:
                pass
        await self.accept()
        await self.send_message_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(*self.group_args)

    async def switch_group(self, group_name):
        await self.channel_layer.group_discard(*self.group_args)
        self.group_name = group_name
        self.group_args = (self.group_name, self.channel_name)
        await self.channel_layer.group_add(*self.group_args)

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
            await self.channel_layer.group_send(self.group_name, {'type': 'chat_message', 'data': data})

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
        await self.channel_layer.group_send(self.group_name, {'type': 'chat_message', 'data': data})

    @database_sync_to_async
    def get_messages(self, offset=0, limit=MESSAGES_LIMIT):
        qs = Message.objects.filter(chat=self.chat).order_by('-timestamp')[offset:limit]
        total = Message.objects.filter(chat=self.chat).count()
        data = get_serializer_data(qs, many=True)
        return data, qs.count(), total
