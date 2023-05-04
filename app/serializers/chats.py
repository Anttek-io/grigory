from app.models import Chat, CHAT_TYPE_PRIVATE, CHAT_TYPE_GROUP
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from app.serializers.users import UserSerializer


class ChatSerializer(serializers.ModelSerializer):
    chat_type_choices = Chat.chat_type_choices
    except_private = list(i[0] for i in chat_type_choices if i[0] != CHAT_TYPE_PRIVATE)
    chat_type = serializers.ChoiceField(choices=except_private, default=CHAT_TYPE_GROUP)
    creator = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        chat_type = attrs.get('chat_type')
        if chat_type == CHAT_TYPE_PRIVATE:
            raise serializers.ValidationError({'chat_type': _('Private chats are created automatically.')})
        return super().validate(attrs)

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

