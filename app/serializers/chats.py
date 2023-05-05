from app.models import Chat, CHAT_TYPE_PRIVATE, CHAT_TYPE_GROUP
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app.serializers.users import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        instance = super().create(validated_data)
        instance.members.add(self.context['request'].user)
        return instance

    class Meta:
        model = Chat
        exclude = ('members',)


class ChatListSerializer(ChatSerializer):
    last_message = serializers.SerializerMethodField(read_only=True)

    def get_last_message(self, obj):
        if obj.last_message:
            from app.serializers.messages import MessageWithoutChatSerializer
            return MessageWithoutChatSerializer(obj.last_message).data
        return None

