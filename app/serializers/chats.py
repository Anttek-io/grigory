from app.models import Chat
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ChatSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].read_only = True

    def validate(self, attrs):
        chat_type = attrs.get('chat_type')
        if chat_type == 'private':
            raise serializers.ValidationError({'chat_type': _('Private chats are created automatically.')})
        return super().validate(attrs)

    class Meta:
        model = Chat
        fields = '__all__'
