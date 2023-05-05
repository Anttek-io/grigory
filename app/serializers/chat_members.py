from rest_framework import serializers

from app.models import ChatMember


class ChatMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMember
        fields = '__all__'
