from rest_framework import serializers

from app.models import Chat
from app.serializers.base import BaseSerializer
from app.serializers.users import UserSerializer


class ChatSerializer(BaseSerializer):
    creator = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.members.add(self.context['request'].user)
        return instance

    class Meta:
        model = Chat
        fields = '__all__'
        create_only_fields = ('chat_type',)


class ChatListSerializer(ChatSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)

    def get_last_message(self, obj) -> dict or None:
        if obj.last_message:
            from app.serializers.messages import MessageWithoutChatSerializer
            return MessageWithoutChatSerializer(obj.last_message).data
        return None

