from rest_framework import serializers

from app.models import ChatMember


class ChatMemberSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        instance = self.instance
        print(instance)
        return attrs

    class Meta:
        model = ChatMember
        fields = '__all__'
