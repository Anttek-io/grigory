from rest_framework import serializers

from app.models import Message
from app.serializers.users import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

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
