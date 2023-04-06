from app.models import Message
from rest_framework import serializers

from app.serializers.chats import ChatSerializer
from app.serializers.sender import SenderSerializer


class MessageSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender_id'].read_only = True
        self.fields['who_seen'].read_only = True

    sender = SenderSerializer(read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('sender_id', None)
        data['chat'] = ChatSerializer(instance.chat).data
        return data

    class Meta:
        model = Message
        fields = '__all__'
