import logging

from channels.layers import get_channel_layer
from rest_framework import serializers

from app.models import Message
from app.serializers.chats import ChatSerializer
from app.serializers.sender import SenderSerializer


class MessageSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender_id'].read_only = True
        self.fields['who_seen'].read_only = True

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['chat'] = ChatSerializer(instance.chat).data
        return data

    async def send_to_websocket(self):
        data = self.data.copy()
        channel_layer = get_channel_layer()
        sender = await self.instance.async_get_sender()
        if sender:
            data['sender'] = SenderSerializer(sender).data
            data.pop('sender_id')
        await channel_layer.group_send(
            self.instance.chat.slug,
            {
                'type': 'chat_message',
                'data': data
            }
        )

    class Meta:
        model = Message
        fields = '__all__'
