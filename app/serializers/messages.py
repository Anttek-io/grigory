from django.db import transaction
from rest_framework import serializers

from app.models import Message, Chat
from app.serializers.chats import ChatSerializer
from app.serializers.messages__attachments import AttachmentSerializer
from app.serializers.users import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    attachments = AttachmentSerializer(many=True, required=False)

    def get_chat_queryset(self):
        if self.context.get('request') and self.context['request'].user.is_authenticated:
            return Chat.objects.filter(members__user=self.context['request'].user)
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
        request = self.context.get('request')
        files = request.FILES.getlist('attachments') if request else None
        if files:
            validated_data['ready'] = False
        try:
            with transaction.atomic():
                instance = super().create(validated_data)
                if request and files:
                    for file in request.FILES.getlist('attachments'):
                        instance.attachments.create(file=file)
                    instance.ready = True
                    instance.save()
        except Exception as e:
            raise serializers.ValidationError(e)
        return instance

    class Meta:
        model = Message
        exclude = ('ready',)


class MessageWithoutChatSerializer(serializers.ModelSerializer):
    chat = None

    class Meta:
        model = Message
        exclude = ('ready',)
