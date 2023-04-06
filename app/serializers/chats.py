from app.models import Chat
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].read_only = True

    class Meta:
        model = Chat
        fields = '__all__'
