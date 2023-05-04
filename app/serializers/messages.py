from rest_framework import serializers

from app.models import Message, Chat
from app.serializers.chats import ChatSerializer
from app.serializers.users import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    def get_chat_queryset(self):
        if self.context.get('request'):
            return self.context['request'].user.chats.all()
        return Chat.objects.none()

    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        kwargs["chat"] = {"queryset": self.get_chat_queryset()}
        return kwargs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['chat'] = ChatSerializer(instance.chat).data
        return data

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)

    class Meta:
        model = Message
        fields = '__all__'


class MessageWithoutChatSerializer(serializers.ModelSerializer):
    chat = None

    class Meta:
        model = Message
        fields = '__all__'
