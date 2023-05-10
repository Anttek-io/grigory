import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Max

from app.models import Chat
from app.serializers.chats import ChatSerializer, ChatListSerializer


def get_user_chats(user):
    qs = Chat.objects.annotate(last_message_timestamp=Max('messages__timestamp')).filter(
        members__user=user).order_by('-last_message_timestamp')
    total = qs.count()
    data = get_serializer_data(qs, many=True)
    chats_list = {
        'type': 'chat_list',
        'count': qs.count(),
        'total': total,
        'results': data
    }
    return chats_list


def get_serializer_data(instance, many=False):
    if many:
        serializer_class = ChatListSerializer
    else:
        serializer_class = ChatSerializer
    serializer = serializer_class(instance, many=many)
    return serializer.data


class ChatsConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.group_args = None
        self.group_name = None
        self.user = None

    async def connect(self):
        self.user = self.scope['user']
        self.group_name = f'user_{self.user.id}_chats'
        self.group_args = (self.group_name, self.channel_name)
        await self.channel_layer.group_add(*self.group_args)
        await self.accept()
        logging.debug(f'User {self.user} connected to {self.group_name}.')
        await self.send_chats_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(*self.group_args)

    async def send_message(self, event):
        assert event.get('data'), 'Data is required'
        await self.send(text_data=json.dumps(event['data']))

    async def send_chats_list(self):
        data = await database_sync_to_async(get_user_chats)(self.user)
        await self.channel_layer.group_send(self.group_name, {'type': 'send_message', 'data': data})
